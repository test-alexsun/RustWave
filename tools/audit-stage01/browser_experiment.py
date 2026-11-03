"""3x controlled / 3x constrained / 3x CPU contention diagnostics."""
import run as h
import sys

OLD=h.RAW
h.RAW=OLD/(sys.argv[1] if len(sys.argv)>1 else 'browser-gaps02')


def main():
    h.RAW.mkdir(exist_ok=True)
    if (h.RAW/'commands.json').exists(): raise SystemExit('Evidence exists')
    profiles=[('cpu-only','1','2000m'),('ram-only','2','1400m')] if len(sys.argv)>2 and sys.argv[2]=='isolate' else [('control','2','2000m'),('constrained','1','1400m'),('contention','1','1400m')]
    for profile,cpu,ram in profiles:
        h.run('browser-'+profile,[h.DOCKER,'run','--rm','--network','none','--cpus',cpu,'--memory',ram,
              '-v',f'{OLD / "source-lf"}:/src:ro',
              '-v',f'{OLD / "source/frontend/node_modules"}:/src/frontend/node_modules',
              '-v',f'{h.ROOT / "tools/audit-stage01"}:/audit:ro','-v',f'{h.RAW}:/evidence',
              '-e','AUDIT_PROFILE='+profile,'-e','TZ=UTC','-e','LC_ALL=C.UTF-8','-w','/src/frontend',
              'rustwave-audit01:tools','bun','/audit/browser_diagnostic.mjs'],timeout=600)


if __name__=='__main__':main()
