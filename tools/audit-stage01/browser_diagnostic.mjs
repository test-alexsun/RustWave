// External diagnostic build: source files remain byte-identical. No assertions removed.
import { build } from '/src/frontend/node_modules/vite/dist/node/index.js'
import { spawn } from 'node:child_process'
import { once } from 'node:events'
import { mkdtempSync, readFileSync, writeFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'

const output=mkdtempSync(join(tmpdir(),'rw-diagnostic-'))
const profile=process.env.AUDIT_PROFILE || 'control'
const result={profile,utc:new Date().toISOString(),deadline_ms:20000,trials:[]}
const stamp=()=>performance.now()
const metric=()=>Object.fromEntries(['cpu.stat','memory.current','memory.peak','memory.events'].map(f=>[f,readFileSync('/sys/fs/cgroup/'+f,'utf8')]))
const buildStart=stamp()
try {
 await build({configFile:'/src/frontend/vite.config.ts',root:'/src/frontend',base:'./',logLevel:'error',
  define:{__BUILD_ID__:JSON.stringify('browser-test')},
  plugins:[{name:'audit-assert-progress',enforce:'pre',transform(code,id){
   if(!id.endsWith('/tests/browser-smoke.tsx')) return
   const needle='if (!condition) throw new Error(message)'
   if(!code.includes(needle)) throw Error('Assertion instrumentation point absent')
   return code.replace(needle,'((window as unknown as {__auditProgress: unknown[]}).__auditProgress ||= []).push({message,pass:Boolean(condition),at:performance.now()}); console.debug("AUDIT_ASSERT",message,Boolean(condition)); '+needle)
  }}],build:{outDir:output,emptyOutDir:true,copyPublicDir:false,rollupOptions:{input:'/src/frontend/tests/browser.html'}}})
 result.build_ms=stamp()-buildStart
 const html=join(output,'tests/browser.html')
 writeFileSync(html,readFileSync(html,'utf8').replace(/(src|href)="([^"]+)"/g,(_m,a,v)=>`${a}="${new URL(v,pathToFileURL(html)).href}"`).replace('<head>','<head><base href="https://gowave.invalid/panel/">'))
 for(let trial=1;trial<=3;trial++) {
  const t={trial,events:[],samples:[],started:new Date().toISOString()};result.trials.push(t)
  let browser,socket,stress;let stderr='';let deadline;const start=stamp()
  try {
   if(profile==='contention') stress=spawn('bun',['-e','while(true){}'],{stdio:'ignore'})
   browser=spawn('chromium',['--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--allow-file-access-from-files','--remote-debugging-port=0',`--user-data-dir=${join(output,'profile-'+trial)}`,'about:blank'],{stdio:['ignore','ignore','pipe']})
   const port=await new Promise((resolve,reject)=>{
    const timer=setTimeout(()=>reject(Error('Chromium startup timed out')),10000)
    browser.once('error',reject)
    browser.stderr.on('data',b=>{stderr+=String(b);const m=stderr.match(/DevTools listening on ws:\/\/127\.0\.0\.1:(\d+)/);if(m){clearTimeout(timer);resolve(m[1])}})
   })
   const pages=await fetch(`http://127.0.0.1:${port}/json/list`).then(r=>r.json())
   socket=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl)
   await new Promise((resolve,reject)=>{socket.onopen=resolve;socket.onerror=reject})
   let serial=0;const pending=new Map()
   socket.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);if(p){clearTimeout(p.timer);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result)}}
    else if(['Runtime.consoleAPICalled','Runtime.exceptionThrown','Network.loadingFailed','Page.loadEventFired','Page.domContentEventFired'].includes(m.method))t.events.push({at_ms:stamp()-start,...m})}
   const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++serial;const timer=setTimeout(()=>{pending.delete(id);reject(Error('CDP call timed out at diagnostic deadline: '+method))},deadline?Math.max(1,deadline-stamp()):10000);pending.set(id,{resolve,reject,timer});socket.send(JSON.stringify({id,method,params}))})
   await call('Runtime.enable');await call('Network.enable');await call('Page.enable')
   const before=stamp();deadline=before+20000;t.before=metric()
   await call('Page.navigate',{url:pathToFileURL(html).href})
   while(stamp()-before<20000){
    const evaluated=await call('Runtime.evaluate',{expression:'JSON.stringify({url:location.href,readyState:document.readyState,result:document.body?.dataset.result,progress:window.__auditProgress||[],text:document.body?.textContent?.slice(0,1000)})',returnByValue:true})
    t.last=JSON.parse(evaluated.result.value);t.samples.push({at_ms:stamp()-before,readyState:t.last.readyState,result:t.last.result,assertions:t.last.progress.length,resources:metric()})
    if(t.last.result){t.status=t.last.result==='passed'?'PASS':'FAIL';break}
    await Bun.sleep(100)
   }
   t.after=metric();t.smoke_ms=stamp()-before;t.status ||= 'FAIL';if(!t.last?.result)t.error='Browser smoke tests timed out (20000ms)'
   t.chromium_stderr=stderr
  }catch(e){t.status='FAIL';t.error=String(e);t.after=metric()}
  finally{
   socket?.close();if(browser&&browser.exitCode===null){browser.kill();await once(browser,'exit')}
   if(stress&&stress.exitCode===null){stress.kill();await once(stress,'exit')}
   t.chromium_stderr=stderr;t.duration_ms=stamp()-start;t.exit_code=t.status==='PASS'?0:1
   writeFileSync(`/evidence/browser-${profile}.json`,JSON.stringify(result,null,2))
  }
 }
}finally{rmSync(output,{recursive:true,force:true})}
console.log(JSON.stringify(result.trials.map(t=>({trial:t.trial,status:t.status,duration_ms:t.duration_ms,assertions:t.last?.progress.length,error:t.error}))))
process.exitCode=result.trials.some(t=>t.status!=='PASS')?1:0
