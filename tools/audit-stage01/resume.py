"""Resume on blob-verified LF archive, preserving all first-attempt evidence."""
import json
from pathlib import Path
import run as harness

R=harness.RAW
D=harness.DOCKER
harness.records=json.loads((R/'commands.json').read_text())
SRC=R/'source-lf'
P='rustwave-audit01-lf'


def main():
    # Never re-extract or overwrite the old CRLF attempt.
    assert SRC.is_dir()
    verification=json.loads((R/'archive-verification.json').read_text())
    assert not verification['upstream-lf.tar']['mismatches']
    if harness.docker('lf-network','network','create','--internal',P): return
    try:
        harness.docker('lf-pg-start','run','-d','--network',P,'--network-alias','pg',
                       '--memory','512m','--cpus','1','--tmpfs','/var/lib/postgresql:rw,size=400m',
                       '-e','POSTGRES_HOST_AUTH_METHOD=trust','-e','POSTGRES_USER=audit','-e','POSTGRES_DB=audit','postgres:18')
        mounts=['-v',f'{SRC}:/src','-v',f'{R}:/evidence']
        base=['run','--rm','--network',P,'--memory','2300m','--cpus','2',*mounts,
              '-e','TZ=UTC','-e','LC_ALL=C.UTF-8','-e','GOMAXPROCS=2','-e','GOCACHE=/evidence/go-cache',
              '-e','GOMODCACHE=/evidence/go-mod','-w','/src/backend-go','golang:1.27.3-bookworm']
        harness.run('lf-go-fmt',[D,*base,'gofmt','-l','.'])
        harness.run('lf-go-fmt-gate',[D,*base,'sh','-c','files=$(gofmt -l .); test -z "$files"'])
        harness.run('lf-go-fmt-diff',[D,*base,'gofmt','-d','.'])
        harness.run('lf-go-vet',[D,*base,'go','vet','./...'])
        for mode in ('sqlite','postgres'):
            env=['-e',f'GOWAVE_PROBE_OUT=/evidence/lf-probe-{mode}.json']
            if mode=='postgres': env+=['-e','GOWAVE_TEST_POSTGRES=postgres://audit@pg:5432/audit?sslmode=disable']
            cmd=base.copy();cmd[2:2]=env
            flags=['-race'] if mode=='sqlite' else []
            harness.run('lf-go-test-'+mode,[D,*cmd,'go','test','-json','-count=1','-p=2',*flags,'./...'])
        # Supplemental unprivileged security test; keep original skips in ledger.
        cmd=base.copy();cmd[2:2]=['--user','10001:10001']
        harness.run('lf-go-nonroot',[D,*cmd,'go','test','-json','-count=1','./internal/system','-run','^TestRootOnlyWritableRejectsServiceAccountFiles$'])
        harness.run('lf-go-build',[D,*base,'sh','-c','CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /evidence/lf-gowave ./cmd/server'])
        # Reuse frozen installed dependencies, not earlier CRLF source files.
        bun=['run','--rm','--memory','1500m','--cpus','2',*mounts,
             '-v',f'{R / "source/frontend/node_modules"}:/src/frontend/node_modules',
             '-w','/src/frontend','oven/bun:1.4.2']
        for task in ('check','typecheck','test','build'):
            harness.run('lf-frontend-'+task,[D,*bun,'bun','run',task],timeout=600)
        for name,command in [
            ('installer','cd /src && bash -n install.sh && bash scripts/tests/installer.sh'),
            ('response-headers','cd /src && bun scripts/tests/response-rule-headers.cjs'),
            ('contract-export','cd /src && bun scripts/export-contract.cjs > /evidence/lf-commands.json.export && diff -u backend-go/internal/contracts/commands.json /evidence/lf-commands.json.export && bun scripts/export-contract.cjs --openapi > /evidence/lf-openapi.json.export && cmp backend-go/internal/contracts/openapi.json /evidence/lf-openapi.json.export'),
            ('contract-probes','cd /src && for f in /evidence/lf-probe-sqlite.json /evidence/lf-probe-sqlite-mutations.json /evidence/lf-probe-postgres.json /evidence/lf-probe-postgres-mutations.json; do bun scripts/validate-contract.cjs "$f" || exit; done'),
        ]:
            harness.run('lf-'+name,[D,*bun,'sh','-c',command],timeout=300)
        harness.docker('lf-image-build','build','--progress=plain','--build-arg','COMMIT_SHA=d709bad01dc0ceacb20012a3afdf528eddfd061f','-t','rustwave-audit01:upstream-lf',str(SRC),timeout=1200)
        harness.docker('lf-image-inspect','image','inspect','rustwave-audit01:upstream-lf','--format','{{json .}}')
    finally:
        harness.docker('lf-pg-stop','rm','-f',harness.PREFIX+'-lf-pg-start')
        harness.docker('lf-network-remove','network','rm',P)


if __name__=='__main__': main()
