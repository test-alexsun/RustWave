"""Exactly 20 independent patched test runs, one Chromium process/profile per container."""
import run as h
import json
OLD=h.RAW
h.RAW=OLD/'patched-v1/results03'
IMAGE='sha256:29642d96c0925e8cc86d66cc09b74f77c5174f64968334fe40418ee40ef8643e'

def main():
    h.RAW.mkdir(parents=True,exist_ok=True)
    if (h.RAW/'commands.json').exists():raise SystemExit('Evidence exists; no automatic reruns')
    if h.docker('patch-preflight','info','--format','{{.ServerVersion}}'):return
    for profile,cpu,ram in [('normal','2','2000m'),('cpu-only','1','2000m'),('ram-only','2','1400m'),('contention','1','1400m')]:
        for n in range(1,6):
            name=f'patched-{profile}-{n}'
            code=h.run(name,[h.DOCKER,'run','--rm','--network','none','--cpus',cpu,'--memory',ram,
               '-v',f'{OLD / "patched-v1/source"}:/src:ro','-v',f'{OLD / "source/frontend/node_modules"}:/src/frontend/node_modules',
               '-v',f'{h.ROOT / "tools/audit-stage01"}:/audit:ro','-v',f'{h.RAW}:/evidence',
               '-e','TZ=UTC','-e','LC_ALL=C.UTF-8','-e','AUDIT_PROFILE='+profile,'-e','AUDIT_RUN_ID='+name,
               '-w','/src/frontend',IMAGE,'bun','/audit/patched_browser_runner.mjs'],timeout=300)
            if code==125: raise SystemExit('Container launch failure; remaining trials NOT_RUN')
            result=h.RAW/(name+'.json')
            if code and not result.exists(): raise SystemExit('Runner failed before result; remaining trials NOT_RUN')
            if result.exists():
                data=json.loads(result.read_text(encoding='utf-8'))
                if any(str(t.get('error','')).startswith(('ReferenceError:','SyntaxError:')) for t in data['trials']): raise SystemExit('Harness programming error; remaining trials NOT_RUN')

if __name__=='__main__':main()
