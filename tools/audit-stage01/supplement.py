"""Additional executions only; immutable full-suite evidence stays untouched."""
import json
import tarfile
import run as h

OLD=h.RAW
h.RAW=OLD/'gaps01'
P='rustwave-audit01-gaps'


def main():
    h.RAW.mkdir(exist_ok=True)
    if (h.RAW/'commands.json').exists():
        raise SystemExit('Evidence exists; refusing overwrite')
    src=h.RAW/'schema-source'
    src.mkdir()
    with tarfile.open(OLD/'upstream-lf.tar') as a: a.extractall(src,filter='data')
    base=['run','--rm','--memory','2300m','--cpus','2','-v',f'{OLD}:/evidence',
          '-e','TZ=UTC','-e','LC_ALL=C.UTF-8','-e','GOMAXPROCS=2',
          '-e','GOCACHE=/evidence/go-cache','-e','GOMODCACHE=/evidence/go-mod',
          '-w','/src/backend-go']
    for mode in ('sqlite','postgres'):
        h.run('schema-'+mode,[h.DOCKER,*base,'--network','none','-v',f'{src}:/src','-e','GOWAVE_EXPORT_SCHEMA=1','golang:1.27.3-bookworm','go','test','-json','-count=1','./internal/database','-run','^TestExportSchema$'],timeout=300)
    h.docker('network','network','create','--internal',P)
    try:
        h.docker('pg','run','-d','--network',P,'--network-alias','pg','--memory','512m','--cpus','1','--tmpfs','/var/lib/postgresql:rw,size=400m','-e','POSTGRES_HOST_AUTH_METHOD=trust','-e','POSTGRES_USER=audit','-e','POSTGRES_DB=audit','postgres:18')
        for mode in ('sqlite','postgres'):
            h.run('migration-'+mode,[h.DOCKER,*base,'--network',P,'-v',f'{OLD / "source-lf"}:/src:ro','-e','GOWAVE_TEST_POSTGRES=postgres://audit@pg:5432/audit?sslmode=disable','golang:1.27.3-bookworm','go','test','-json','-count=1','./internal/cli','./internal/database','-run','^(TestMigrateSQLiteToPostgres_Integration|TestMigrationsFreshAndExisting|TestBrandingMigrationPreservesCustomTitles)$'],timeout=300)
    finally:
        h.docker('pg-stop','rm','-f',h.PREFIX+'-pg')
        h.docker('net-stop','network','rm',P)


if __name__=='__main__': main()
