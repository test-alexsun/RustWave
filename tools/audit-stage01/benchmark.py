"""Fresh empty-DB idle baseline; Docker Desktop only; no remote hosts.

Image must be built by run.py. Uses only newly created labelled resources.
CPU is cgroup usage_usec delta / monotonic interval, 100% = one CPU.
Startup includes Docker start + local HTTP polling overhead, not pure Run().
"""
from pathlib import Path
import json
import os
import secrets
import subprocess
import time
import urllib.request
import urllib.error
import datetime

ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/'docs/benchmarks/raw'
D=r'C:\Program Files\Docker\Docker\resources\bin\docker.exe'
os.environ['PATH']=str(Path(D).parent)+os.pathsep+os.environ['PATH']
P='rustwave-audit01-bench'
IMAGE='rustwave-audit01:upstream-lf'


def d(*args,check=True):
    p=subprocess.run([D,*args],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if check and p.returncode:
        raise RuntimeError('docker '+args[0]+': '+p.stderr)
    return p.stdout.strip()


def sample(name):
    # PostgreSQL RSS is only its PID 1; cgroup memory covers every DB worker.
    text=d('exec',name,'sh','-c', 'cat /proc/1/status; cat /sys/fs/cgroup/cpu.stat; echo CGROUP_MEMORY; cat /sys/fs/cgroup/memory.current; cat /sys/fs/cgroup/memory.stat')
    fields={}
    for line in text.splitlines():
        v=line.replace(':','').split()
        if len(v)==2 and v[1].isdigit(): fields[v[0]]=int(v[1])
        if len(v)==3 and v[2]=='kB': fields[v[0]]=int(v[1])*1024
    fields['memory_current']=int(text.split('CGROUP_MEMORY\n')[1].splitlines()[0])
    return fields


def fetch(base,path,method='GET',headers=None):
    # Internal Docker bridges do not publish ports in this Desktop version.
    # An idle probe sidecar stays inside that network; no host/external access.
    try:
        code='const [url,method,headers]=JSON.parse(process.argv[1]); try { const r=await fetch(url,{method,headers,signal:AbortSignal.timeout(2000)}); console.log(JSON.stringify({status:r.status,headers:Object.fromEntries(r.headers),body:await r.text()})); } catch(e) { console.log(JSON.stringify({status:"CONNECTION_ERROR",error:e.name})); }'
        proc=subprocess.run([D,'exec',P+'-probe','bun','-e',code,json.dumps([base+path,method,headers or {}])],capture_output=True,text=True,timeout=10)
        return json.loads(proc.stdout)
    except Exception as e:
        return dict(status='CONNECTION_ERROR',error=type(e).__name__)


def main():
    if (RAW/'baseline.json').exists():
        raise SystemExit('Existing measurements preserved; use a separate evidence directory for a new run.')
    inspected=json.loads(d('image','inspect',IMAGE))[0]
    result={'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'image':inspected['Id'],'image_bytes':inspected['Size'], 'host':json.loads(d('info','--format','{{json .}}'))['OperatingSystem'], 'modes':{},'method':'3 fresh backend starts/mode; 20s warmup; 30s idle window; no users/nodes; 1 CPU 256MiB app, 1 CPU 512MiB PG; metrics enabled'}
    names=[]
    created_net=False
    try:
        d('network','create','--internal',P); created_net=True
        probe=P+'-probe'; names.append(probe)
        d('run','-d','--name',probe,'--network',P,'--memory','256m','--cpus','1','--read-only','--cap-drop','ALL','rustwave-audit01:tools','bun','-e','setInterval(()=>{},60000)')
        for mode in ('sqlite','postgres'):
            pg=None
            if mode=='postgres':
                pg=P+'-pg'; names.append(pg)
                d('create','--name',pg,'--network',P,'--memory','512m','--cpus','1','--tmpfs','/var/lib/postgresql:rw,size=400m','-e','POSTGRES_HOST_AUTH_METHOD=trust','-e','POSTGRES_USER=audit','-e','POSTGRES_DB=audit','postgres:18')
                start=time.monotonic(); d('start',pg)
                ready=False
                for _ in range(120):
                    p=subprocess.run([D,'exec',pg,'pg_isready','-U','audit','-d','audit'],capture_output=True)
                    if p.returncode==0: ready=True; break
                    time.sleep(.1)
                if not ready: raise RuntimeError('PG not ready')
                result['pg_startup_seconds']=time.monotonic()-start
            trials=[]
            for i in range(3):
                # Reset PostgreSQL database between trials; this is this script's own instance.
                if pg and i:
                    d('exec',pg,'psql','-U','audit','-d','postgres','-c','DROP DATABASE audit;')
                    d('exec',pg,'psql','-U','audit','-d','postgres','-c','CREATE DATABASE audit;')
                app=P+'-'+mode+'-'+str(i); names.append(app)
                secret=secrets.token_hex(32)  # Never written to result files or command log.
                env=['-e','APP_SECRET='+secret,'-e','DB_DRIVER='+mode,'-e','DATABASE_URL='+('/tmp/gowave.db' if mode=='sqlite' else 'postgres://audit@'+pg+':5432/audit?sslmode=disable'),'-e','METRICS_USER=audit','-e','METRICS_PASS='+secret,'-e','TZ=UTC']
                d('create','--name',app,'--network',P,'--memory','256m','--cpus','1','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--tmpfs','/tmp:rw,size=64m',*env,IMAGE)
                start=time.monotonic(); d('start',app)
                base='http://'+app+':3000'
                metrics='http://'+app+':3001'
                ready=False
                for _ in range(200):
                    if fetch(base,'/api/system/health')['status']==200: ready=True; break
                    time.sleep(.05)
                if not ready: raise RuntimeError('backend not healthy')
                startup=time.monotonic()-start
                time.sleep(20)
                before=sample(app); dbefore=sample(pg) if pg else None
                t=time.monotonic(); time.sleep(30)
                after=sample(app); dafter=sample(pg) if pg else None
                elapsed=time.monotonic()-t
                trial={'startup_seconds':startup,'idle_seconds':elapsed,'backend_rss_bytes':after['VmRSS'],'backend_cgroup_bytes':after['memory_current'],'backend_cpu_percent':(after['usage_usec']-before['usage_usec'])/1e6/elapsed*100,'backend_before':before,'backend_after':after}
                if mode=='sqlite' and i==0:
                    d('cp',app+':/app/gowave',str(RAW/'gowave-image'))
                    result['image_binary_bytes']=(RAW/'gowave-image').stat().st_size
                if pg: trial['database']={'cgroup_bytes':dafter['memory_current'],'pid1_rss_bytes':dafter['VmRSS'],'cpu_percent':(dafter['usage_usec']-dbefore['usage_usec'])/1e6/elapsed*100,'before':dbefore,'after':dafter}
                else: trial['database']={'separate_process':'none: SQLite is inside backend RSS/CPU; no honest separate RSS attribution'}
                trials.append(trial)
                if i==0:
                    import base64
                    auth='Basic '+base64.b64encode(('audit:'+secret).encode()).decode()
                    trial['http_smoke']={path:fetch(base,path) for path in ['/','/dashboard/home','/api/unknown-audit-path','/assets/missing-audit.js','/missing-audit.html','/api/users']}
                    trial['head']=fetch(base,'/dashboard/home','HEAD')
                    trial['metrics_unauthorized']=fetch(metrics,'/metrics')
                    trial['metrics_authorized']=fetch(metrics,'/metrics',headers={'Authorization':auth})
                    trial['metrics_health']=fetch(metrics,'/health')
                    trial['metrics_wrong_method']=fetch(metrics,'/metrics','POST')
                    # Full public metrics text contains only synthetic empty-instance values.
                    (RAW/('metrics-'+mode+'.txt')).write_text(trial['metrics_authorized']['body'],encoding='utf-8')
                d('rm','-f',app); names.remove(app)
                result['modes'][mode]=trials
                (RAW/'baseline.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
                print(mode,i,round(startup,3),after['VmRSS'],round(trial['backend_cpu_percent'],3),flush=True)
            # Enabled/disabled is a separate smoke check, outside idle windows.
            disabled=P+'-'+mode+'-disabled'; names.append(disabled)
            env=['-e','APP_SECRET='+secrets.token_hex(32),'-e','DB_DRIVER='+mode,'-e','DATABASE_URL='+('/tmp/disabled.db' if mode=='sqlite' else 'postgres://audit@'+pg+':5432/audit?sslmode=disable'),'-e','METRICS_ENABLED=false']
            d('run','-d','--name',disabled,'--network',P,'--memory','256m','--cpus','1','--read-only','--tmpfs','/tmp:rw,size=64m',*env,IMAGE)
            for _ in range(60):
                check=subprocess.run([D,'exec',disabled,'wget','-q','-O','/dev/null','http://127.0.0.1:3000/api/system/health'],capture_output=True)
                if check.returncode==0:break
                time.sleep(.1)
            metriccheck=subprocess.run([D,'exec',disabled,'wget','-q','-T','2','-O','/dev/null','http://127.0.0.1:3001/health'],capture_output=True)
            result.setdefault('metrics_disabled',{})[mode]={'api_health_exit':check.returncode,'metrics_health_exit':metriccheck.returncode,'pass':check.returncode==0 and metriccheck.returncode!=0}
            d('rm','-f',disabled); names.remove(disabled)
            (RAW/'baseline.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            if pg: d('rm','-f',pg); names.remove(pg)
    finally:
        for name in names: d('rm','-f',name,check=False)
        if created_net: d('network','rm',P,check=False)


if __name__=='__main__': main()
