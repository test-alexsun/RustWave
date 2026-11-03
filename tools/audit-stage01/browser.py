"""Supplemental browser/branding checks with explicit git and Chromium tools."""
import run as h

ORIGINAL_RAW=h.RAW
h.RAW=ORIGINAL_RAW/'extra'
h.RAW.mkdir(exist_ok=True)
SRC=ORIGINAL_RAW/'source-lf'
IMAGE='rustwave-audit01:tools'


def main():
    if h.docker('tools-build','build','-f',str(h.ROOT/'tools/audit-stage01/Dockerfile.tools'),'-t',IMAGE,str(h.ROOT/'tools/audit-stage01'),timeout=900):return
    mounts=['-v',f'{SRC}:/src','-v',f'{ORIGINAL_RAW / "source/frontend/node_modules"}:/src/frontend/node_modules']
    base=['run','--rm','--memory','1400m','--cpus','1',*mounts,'-w','/src',IMAGE]
    h.run('browser-versions',[h.DOCKER,*base,'sh','-c','bun --version && chromium --version && git --version'])
    # Branding tool needs a Git worktree inventory. This isolated snapshot has
    # no remote and no commits; no original checkout or Git config is modified.
    h.run('lf-branding',[h.DOCKER,*base,'sh','-c','git init -q && git config --local core.autocrlf false && git add . && bun scripts/check-branding.cjs'],timeout=180)
    h.run('lf-browser',[h.DOCKER,*base,'sh','-c','cd frontend && bun run test:browser'],timeout=300)


if __name__=='__main__':main()
