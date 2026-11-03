"""Bounded original-vs-external smoke checks, immutable source and old evidence."""
import run as h
import sys
OLD=h.RAW
h.RAW=OLD/(sys.argv[1] if len(sys.argv)>1 else 'readiness02')

def main():
    h.RAW.mkdir(exist_ok=True)
    if (h.RAW/'commands.json').exists(): raise SystemExit('Evidence exists')
    if h.docker('preflight','info','--format','{{.ServerVersion}} {{.OperatingSystem}}'): return
    mounts=['-v',f'{OLD / "source-lf"}:/src:ro','-v',f'{OLD / "source/frontend/node_modules"}:/src/frontend/node_modules',
            '-v',f'{h.ROOT / "tools/audit-stage01"}:/audit:ro','-v',f'{h.RAW}:/evidence']
    base=['run','--rm','--network','none',*mounts,'-e','TZ=UTC','-e','LC_ALL=C.UTF-8','-w','/src/frontend']
    for n in range(1,4):
        h.run('original-'+str(n),[h.DOCKER,*base,'--cpus','2','--memory','2000m','rustwave-audit01:tools','bun','run','test:browser'],timeout=300)
    for profile,cpu,ram in [('control','2','2000m'),('cpu-only','1','2000m'),('ram-only','2','1400m'),('contention','1','1400m')]:
        h.run('external-'+profile,[h.DOCKER,*base,'--cpus',cpu,'--memory',ram,'-e','AUDIT_PROFILE='+profile,'rustwave-audit01:tools','bun','/audit/browser_deterministic.mjs'],timeout=600)

if __name__=='__main__':main()
