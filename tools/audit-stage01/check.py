"""Audit artifact completeness and pinned-source preservation, not parity proof."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
from inventory import ROOT, DOC, OUT, read


def main():
    required=['stages/STAGE_01_AUDIT.md','ARCHITECTURE_BASELINE.md','FUNCTIONAL_PARITY_MATRIX.md',
              'benchmarks/GO_BASELINE.md','TEST_INVENTORY.md','PROGRESS.md','HANDOFF.md',
              'FRONTEND_API_SHAPE_MATRIX.md','FRONTEND_API_PARITY.md','STATIC_SERVING_PARITY.md','METRICS_PARITY.md']
    errors=[]
    for f in required:
        if not (DOC/f).is_file():errors.append('Missing '+f)
    for p in (ROOT/'tools/audit-stage01').glob('*.py'): ast.parse(read(p))
    for p in OUT.glob('*.json'): json.loads(read(p))
    counts=json.loads(read(OUT/'counts.json'))
    routes=json.loads(read(OUT/'routes.json'))
    calls=json.loads(read(OUT/'frontend-calls.json'))
    manifest=json.loads(read(OUT/'go-test-manifest.json'))
    assert len(routes)==counts['api_operations']==248
    assert len(calls)==counts['frontend_calls']==221
    assert len(manifest)==counts['go_tests']==128
    assert len({r['id'] for r in routes})==len(routes)
    assert len({r['id'] for r in calls})==len(calls)
    assert len({r['id'] for r in manifest})==len(manifest)
    assert counts['feature_items']==counts['api_operations']+counts['capability_groups']==304
    for x in routes+calls+manifest:
        if x.get('source'):
            f,line=x['source'].rsplit(':',1)
            assert (ROOT/f).is_file() and 0<int(line)<=len(read(ROOT/f).splitlines())
    git=['git','-c','safe.directory='+ROOT.as_posix()]
    upstream='d709bad01dc0ceacb20012a3afdf528eddfd061f'
    preserved=['backend-go','frontend','scripts','Dockerfile','docker-compose.yml','docker-compose.build.yml','install.sh','.github','LICENSE']
    p=subprocess.run(git+['diff','--exit-code',upstream,'--',*preserved],cwd=ROOT,capture_output=True)
    if p.returncode:errors.append('Original source differs from lock SHA')
    p=subprocess.run(git+['diff','--check'],cwd=ROOT,capture_output=True)
    if p.returncode:errors.append('git diff --check failed')
    # Verify current LF original files after tests/build; generated dist/.git are not source blobs.
    tree=subprocess.check_output(git+['ls-tree','-rz',upstream],cwd=ROOT)
    checked=0
    for row in tree.split(b'\x00'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,kind,sha=meta.split()
        if kind!=b'blob':continue
        p=DOC/'benchmarks/raw/source-lf'/name.decode()
        data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if actual!=sha.decode():errors.append('LF source mutated: '+name.decode())
        checked+=1
    # Local links only; schemas' JSON descriptions are not scanned as Markdown.
    targets=[DOC/f for f in required]+[OUT/'FRONTEND_CUSTOM.md',OUT/'ARCHIVE_INTEGRITY.md']
    for p in targets:
        for link in re.findall(r'\]\(([^)]+)\)',read(p)):
            if '://' in link or link.startswith('#'):continue
            dest=link.split('#')[0]
            if not (p.parent/dest).exists():errors.append(f'Broken link {p.name}: {link}')
    result={'required_reports':len(required),'source_blobs_checked':checked,'api_operations':len(routes),
            'frontend_calls':len(calls),'expected_go_ids_per_mode':len(manifest),'errors':errors,'status':'FAIL' if errors else 'PASS'}
    (OUT/'artifact-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
    if errors:raise SystemExit(1)


if __name__=='__main__':main()
