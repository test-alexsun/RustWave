"""Create reproducible test-only patch and apply it to a new pinned archive copy."""
from pathlib import Path
import difflib, hashlib, json, subprocess, tarfile
ROOT=Path(__file__).resolve().parents[2]
TOOLS=Path(__file__).parent
RAW=ROOT/'docs/benchmarks/raw'
SHA='d709bad01dc0ceacb20012a3afdf528eddfd061f'

def main():
    dest=RAW/'patched-v1/source'
    if dest.exists():raise SystemExit('Existing patched evidence preserved')
    original=(RAW/'source-lf/frontend/tests/browser-smoke.tsx').read_text(encoding='utf-8')
    helper='''
type AuditWindow = Window & {
    __auditProgress?: { message: string; pass: boolean; at: number }[]
    __auditReadiness?: { label: string; at: number; value?: number }[]
}
const auditWindow = window as AuditWindow
const auditMark = (label: string, value?: number) => {
    ;(auditWindow.__auditReadiness ||= []).push({ label, at: performance.now(), value })
}
async function waitForAuditState(predicate: () => boolean, label: string): Promise<void> {
    if (predicate()) { auditMark(label); return }
    await new Promise<void>((resolve, reject) => {
        let finished = false
        let frame = 0
        const finish = (error?: Error) => {
            if (finished) return
            finished = true
            observer.disconnect()
            cancelAnimationFrame(frame)
            clearTimeout(timer)
            if (error) reject(error)
            else { auditMark(label); resolve() }
        }
        const check = () => {
            if (finished) return
            if (predicate()) finish()
            else frame = requestAnimationFrame(check)
        }
        const observer = new MutationObserver(() => { if (predicate()) finish() })
        const timer = setTimeout(() => finish(new Error('Readiness deadline: ' + label)), 19000)
        observer.observe(document.documentElement, { subtree: true, childList: true, attributes: true, characterData: true })
        frame = requestAnimationFrame(check)
    })
}
'''
    modified=original.replace('function assert(condition: unknown, message: string): void {',helper+'\nfunction assert(condition: unknown, message: string): void {\n    ;(auditWindow.__auditProgress ||= []).push({ message, pass: Boolean(condition), at: performance.now() })')
    before='    flushSync(() => showInbound.click())\n    await wait()'
    after='''    flushSync(() => showInbound.click())
    await waitForAuditState(() => {
        const dialog = document.querySelector('[role="dialog"]')
        return dialog instanceof HTMLElement && dialog.getBoundingClientRect().width > 0 &&
            getComputedStyle(dialog).visibility !== 'hidden' &&
            Boolean(dialog.querySelector('.jer-editor-container .jer-value-string'))
    }, 'modal-viewer-committed')'''
    assert before in modified;modified=modified.replace(before,after)
    before='''    flushSync(() => root.render(<ClockFixture />))
    const firstTime = Number(container.textContent)
    await wait(60)'''
    after='''    const nativeInterval = window.setInterval
    let clockRegistered = false
    let clockDelivered = false
    window.setInterval = ((handler: TimerHandler, delay?: number, ...args: unknown[]) => {
        if (delay !== 20 || typeof handler !== 'function') return nativeInterval(handler, delay, ...args)
        clockRegistered = true
        auditMark('real-clock-registered', delay)
        return nativeInterval(() => {
            clockDelivered = true
            auditMark('real-clock-callback', Date.now())
            handler(...args)
        }, delay)
    }) as typeof window.setInterval
    let firstTime = 0
    try {
        flushSync(() => root.render(<ClockFixture />))
        firstTime = Number(container.textContent)
        auditMark('real-clock-initial-dom', firstTime)
        await waitForAuditState(() => clockRegistered && clockDelivered &&
            Number(container.textContent) > firstTime, 'real-clock-dom-advanced')
    } finally {
        window.setInterval = nativeInterval
    }'''
    assert before in modified;modified=modified.replace(before,after)
    patch=''.join(difflib.unified_diff(original.splitlines(True),modified.splitlines(True),fromfile='a/frontend/tests/browser-smoke.tsx',tofile='b/frontend/tests/browser-smoke.tsx',n=0))
    patchpath=TOOLS/'browser-smoke-v1.patch';patchpath.write_text(patch,encoding='utf-8',newline='\n')
    dest.mkdir(parents=True)
    with tarfile.open(RAW/'upstream-lf.tar') as archive:archive.extractall(dest,filter='data')
    (dest/'frontend/node_modules').mkdir(exist_ok=True)
    subprocess.run(['git','-c','core.autocrlf=true','apply','--unidiff-zero','--check',str(patchpath)],cwd=dest,check=True)
    subprocess.run(['git','-c','core.autocrlf=true','apply','--unidiff-zero',str(patchpath)],cwd=dest,check=True)
    assert (dest/'frontend/tests/browser-smoke.tsx').read_text(encoding='utf-8')==modified
    reference=json.loads((ROOT/'docs/audit/browser-readiness.json').read_text(encoding='utf-8'))['external_trials'][0]['last']['progress']
    assertions=[dict(id=f'BROWSER-A{i:02}',message=a['message']) for i,a in enumerate(reference,1)]
    assert len(assertions)==59
    identity=dict(original_id='GOWAVE-BROWSER-ORIGINAL-'+SHA,patched_id='RUSTWAVE-BROWSER-PATCH-V1',upstream_sha=SHA,patch_sha256=hashlib.sha256(patchpath.read_bytes()).hexdigest(),changed_files=['frontend/tests/browser-smoke.tsx'],runner_unchanged=True,clock='real native setInterval and Date.now; bounded actual DOM advancement',assertions=assertions)
    (TOOLS/'browser-smoke-v1.identity.json').write_text(json.dumps(identity,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in identity.items() if k!='assertions'}))

if __name__=='__main__':main()
