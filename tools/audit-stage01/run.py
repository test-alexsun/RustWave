"""Isolated, local-only Stage 01 evidence. Never runs installers or touches VPS.

Run from repository root with Python 3.13 and Docker Desktop available in PATH.
All mutable upstream build inputs are extracted from git archive into ignored raw/.
"""
import datetime
import json
import os
from pathlib import Path
import subprocess
import tarfile
import time

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / 'docs/benchmarks/raw'
RAW.mkdir(parents=True, exist_ok=True)
DOCKER = r'C:\Program Files\Docker\Docker\resources\bin\docker.exe'
os.environ['PATH'] = str(Path(DOCKER).parent) + os.pathsep + os.environ['PATH']
PREFIX = 'rustwave-audit01'
records = []


def run(name, args, timeout=1800):
    start = time.monotonic()
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    owned_container = None
    if len(args)>2 and args[0]==DOCKER and args[1]=='run':
        owned_container=PREFIX+'-'+name.replace('_','-')
        args=args[:2]+['--name',owned_container]+args[2:]
    try:
        p = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=timeout)
        code, stdout, stderr = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        code, stdout, stderr = 124, e.stdout or b'', e.stderr or b''
        if owned_container:
            subprocess.run([DOCKER,'rm','-f',owned_container],capture_output=True)
    (RAW / (name + '.stdout')).write_bytes(stdout)
    (RAW / (name + '.stderr')).write_bytes(stderr)
    item = dict(name=name, command=args, exit=code, seconds=round(time.monotonic()-start, 3), utc=stamp)
    records.append(item)
    (RAW / 'commands.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
    print(name, code, item['seconds'], flush=True)
    return code


def docker(name, *args, **kwargs):
    return run(name, [DOCKER, *args], **kwargs)


def main():
    if (RAW/'commands.json').exists():
        raise SystemExit('Existing evidence is preserved. Use resume.py for the LF continuation; use a new evidence directory for a fresh run.')
    src = RAW / 'source'
    src.mkdir(exist_ok=True)
    # git -c core.autocrlf=false archive: Windows Git otherwise rewrites LF.
    with tarfile.open(RAW / 'upstream-lf.tar') as archive:
        archive.extractall(src, filter='data')
    # No production volumes, fixed-name upstream compose networks, or host ports.
    if docker('network', 'network', 'create', '--internal', PREFIX):
        return
    docker('pg-start', 'run', '-d', '--name', PREFIX+'-pg', '--network', PREFIX,
           '--memory', '512m', '--cpus', '1', '--tmpfs', '/var/lib/postgresql:rw,size=400m',
           '-e', 'POSTGRES_HOST_AUTH_METHOD=trust', '-e', 'POSTGRES_USER=audit',
           '-e', 'POSTGRES_DB=audit', 'postgres:18')
    mounts = ['-v', f'{src}:/src', '-v', f'{RAW}:/evidence']
    base = ['run', '--rm', '--memory', '2300m', '--cpus', '2', *mounts,
            '-e', 'TZ=UTC', '-e', 'LC_ALL=C.UTF-8', '-e', 'GOMAXPROCS=2',
            '-e', 'GOCACHE=/evidence/go-cache', '-e', 'GOMODCACHE=/evidence/go-mod',
            '-w', '/src/backend-go', 'golang:1.27.3-bookworm']
    run('go-version', [DOCKER, *base, 'go', 'version'])
    run('go-download', [DOCKER, *base, 'go', 'mod', 'download'])
    # Once dependencies are cached, tests have access only to their isolated DB.
    base[2:2] = ['--network', PREFIX]
    run('go-list', [DOCKER, *base, 'go', 'test', '-list', '.', './...'])
    run('go-vet', [DOCKER, *base, 'go', 'vet', './...'])
    run('go-fmt', [DOCKER, *base, 'gofmt', '-l', '.'])
    for mode in ('sqlite', 'postgres'):
        env = ['-e', f'GOWAVE_PROBE_OUT=/evidence/probe-{mode}.json']
        if mode == 'postgres':
            env += ['-e', 'GOWAVE_TEST_POSTGRES=postgres://audit@rustwave-audit01-pg:5432/audit?sslmode=disable']
        cmd = base.copy()
        cmd[2:2] = env
        flags = ['-race'] if mode == 'sqlite' else []
        run('go-test-'+mode, [DOCKER, *cmd, 'go', 'test', '-json', '-count=1', '-p=2', *flags, './...'])
    run('go-build', [DOCKER, *base, 'sh', '-c', 'CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /evidence/gowave ./cmd/server'])
    bun = ['run', '--rm', '--memory', '1500m', '--cpus', '2', *mounts, '-w', '/src/frontend', 'oven/bun:1.4.2']
    run('bun-install', [DOCKER, *bun, 'bun', 'install', '--frozen-lockfile'])
    for task in ('check', 'typecheck', 'test', 'build'):
        run('frontend-'+task, [DOCKER, *bun, 'bun', 'run', task])
    for name, command in [
        ('branding', 'cd /src && bun scripts/check-branding.cjs'),
        ('installer', 'cd /src && bash -n install.sh && bash scripts/tests/installer.sh'),
        ('response-headers', 'cd /src && bun scripts/tests/response-rule-headers.cjs'),
        ('contract-export', 'cd /src && bun scripts/export-contract.cjs > /evidence/commands.json.export && diff -u backend-go/internal/contracts/commands.json /evidence/commands.json.export && bun scripts/export-contract.cjs --openapi > /evidence/openapi.json.export && cmp backend-go/internal/contracts/openapi.json /evidence/openapi.json.export'),
        ('contract-probes', 'cd /src && for f in /evidence/probe-sqlite.json /evidence/probe-sqlite-mutations.json /evidence/probe-postgres.json /evidence/probe-postgres-mutations.json; do bun scripts/validate-contract.cjs "$f" || exit; done'),
        ('browser', 'cd /src/frontend && bun run test:browser'),
    ]:
        run(name, [DOCKER, *bun, 'sh', '-c', command])
    docker('image-build', 'build', '--progress=plain', '--build-arg', 'COMMIT_SHA=d709bad01dc0ceacb20012a3afdf528eddfd061f', '-t', PREFIX+':upstream', str(src))
    docker('image-inspect', 'image', 'inspect', PREFIX+':upstream', '--format', '{{json .}}')
    docker('pg-stop', 'rm', '-f', PREFIX+'-pg')
    docker('network-remove', 'network', 'rm', PREFIX)


if __name__ == '__main__':
    main()
