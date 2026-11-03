"""Fail-closed gate for the owner's approved browser baseline; no baseline generation."""
import argparse
import copy
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / 'tools/audit-stage01'
MANIFEST = TOOLS / 'browser-v1.manifest.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def git(*args):
    return subprocess.check_output(['git', '-c', 'safe.directory=' + ROOT.as_posix(), *args], cwd=ROOT)


def load_manifest():
    m = read_json(MANIFEST)
    require(m['id'] == 'RUSTWAVE-BROWSER-PATCH-V1', 'Unapproved test ID')
    require(m['patch_sha256'] == '0cae2b9c7a6800a6b1c9be9645d438a8beecbce62003f978b4ccbf333c4abf88', 'Unapproved patch')
    require(m['upstream_sha'] == 'd709bad01dc0ceacb20012a3afdf528eddfd061f', 'Unapproved upstream')
    require(len(m['assertions']) == 59 and [a['id'] for a in m['assertions']] == [f'BROWSER-A{i:02}' for i in range(1, 60)], 'Assertion IDs/count')
    for file, expected in m['artifact_lf_sha256'].items():
        require(digest((ROOT / file).read_bytes().replace(b'\r\n', b'\n')) == expected, 'Artifact integrity: ' + file)
    require(digest((TOOLS / 'browser-smoke-v1.patch').read_bytes().replace(b'\r\n', b'\n')) == m['patch_sha256'], 'Patch integrity')
    identity = read_json(TOOLS / 'browser-smoke-v1.identity.json')
    require(identity['assertions'] == m['assertions'], 'Identity assertion drift')
    return m


def verify_case(data, exit_code, profile, patch_hash, m):
    require(exit_code == 0, 'Nonzero process exit')
    require(data.get('identity') == m['id'] and data.get('patch_sha256') == patch_hash, 'Wrong executed baseline')
    require(data.get('profile') == profile and data.get('deadline_ms') == 20000, 'Profile/deadline drift')
    require(len(data.get('trials', [])) == 1, 'Missing/duplicate trial')
    t = data['trials'][0]
    require(t.get('status') == 'PASS' and t.get('exit_code') == 0 and not t.get('error'), 'Failed/unknown trial')
    require(0 < t.get('smoke_ms', 0) <= 20000, 'Missing/exceeded deadline')
    last = t.get('last', {})
    require(last.get('result') == 'passed' and last.get('readyState') == 'complete', 'Page not complete')
    progress = last.get('progress', [])
    require(len(progress) == 59, 'Missing/extra assertions')
    for expected, actual in zip(m['assertions'], progress):
        require(actual.get('message') == expected['message'] and actual.get('pass') is True, 'Assertion failed/skipped/reordered: ' + expected['id'])
    require(all(a.get('at', -1) >= 0 for a in progress), 'Missing assertion timestamps')
    require(all(a['at'] <= b['at'] for a, b in zip(progress, progress[1:])), 'Assertion order')
    trace = last.get('readiness', [])
    marks = {x['label']: x for x in trace}
    needed = ['modal-viewer-committed', 'real-clock-registered', 'real-clock-initial-dom', 'real-clock-callback', 'real-clock-dom-advanced']
    require(all(k in marks for k in needed), 'Missing actual readiness/timer evidence')
    require(marks['modal-viewer-committed']['at'] <= progress[0]['at'], 'Viewer assertion before commit')
    require(marks['real-clock-registered'].get('value') == 20, 'Wrong timer registration')
    initial = marks['real-clock-initial-dom']
    advanced = marks['real-clock-dom-advanced']
    require(any(x['label'] == 'real-clock-callback' and initial['at'] <= x['at'] <= advanced['at'] and x['value'] > initial['value'] for x in trace), 'No advancing real callback before DOM commit')
    require(advanced['at'] <= progress[20]['at'], 'Clock assertion before commit')
    require(not any(e['method'] in ['Runtime.exceptionThrown', 'Network.loadingFailed'] for e in t.get('events', [])), 'Unexpected page exception/network failure')
    require(any(e['method'] == 'Page.loadEventFired' for e in t.get('events', [])), 'Missing page load event')
    for phase in ('before', 'after'):
        require(all(k in t.get(phase, {}) for k in ['cpu.stat', 'memory.current', 'memory.peak', 'memory.events']), 'Missing resource evidence')
    for line in t['after']['memory.events'].splitlines():
        key, value = line.split()
        if key in ('oom', 'oom_kill'):
            require(int(value) == 0, 'OOM during test')
    return {'status': 'PASS', 'expected': 59, 'executed': 59, 'passed': 59, 'failed': 0, 'skipped': 0, 'not_run': 0, 'flaky': 0}


def verify_source(source, m, patched=False):
    checked = 0
    for row in git('ls-tree', '-rz', m['upstream_sha']).split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        _, kind, blob = meta.split()
        if kind != b'blob':
            continue
        rel = name.decode()
        data = (source / rel).read_bytes()
        if patched and rel == 'frontend/tests/browser-smoke.tsx':
            require(digest(data) == m['tested_tsx_sha256'], 'Patched TSX differs from 20 tested runs')
        else:
            require(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == blob.decode(), 'Upstream file changed: ' + rel)
        checked += 1
    require(checked == 1772, 'Source count drift')
    return checked


def prepare(destination, m):
    require(not destination.exists(), 'Refusing to overwrite evidence')
    destination.mkdir(parents=True)
    source = destination / 'source'
    source.mkdir()
    archive = git('-c', 'core.autocrlf=false', 'archive', m['upstream_sha'])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(source, filter='data')
    verify_source(source, m)
    original = source / 'frontend/tests/browser-smoke.tsx'
    (destination / 'original-smoke.tsx').write_bytes(original.read_bytes())
    audit = destination / 'audit'
    audit.mkdir()
    for name in ['browser-smoke-v1.patch', 'browser-smoke-v1.identity.json', 'patched_browser_runner.mjs', 'approved_assertions.cjs']:
        data = (TOOLS / name).read_bytes().replace(b'\r\n', b'\n')
        if name == 'patched_browser_runner.mjs':
            data = data.replace(b'\n', b'\r\n')
            require(digest(data) == m['tested_runner_sha256'], 'Runner differs from 20 tested runs')
        (audit / name).write_bytes(data)
    # A standalone temporary repository prevents parent-checkout path interpretation.
    subprocess.run(['git', 'init', '-q', str(source)], check=True)
    subprocess.run(['git', '-c', 'core.autocrlf=false', 'apply', '--unidiff-zero', str(audit / 'browser-smoke-v1.patch')], cwd=source, check=True)
    # Reproduce the exact Windows execution bytes, without changing any other file.
    original.write_bytes(original.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
    verify_source(source, m, patched=True)
    (source / 'frontend/node_modules').mkdir()
    (destination / 'deps').mkdir()
    (destination / 'results').mkdir()
    save(destination / 'integrity.json', {'status': 'PASS', 'source_files': 1772, 'only_changed_file': 'frontend/tests/browser-smoke.tsx', 'patched_tsx_sha256': digest(original.read_bytes()), 'runner_sha256': m['tested_runner_sha256']})


def negative_tests(m):
    historical = read_json(ROOT / 'docs/audit/browser-patch-v1-results.json')
    case = historical['trials'][0]
    good = {'identity': m['id'], 'patch_sha256': m['patch_sha256'], 'profile': case['profile'], 'deadline_ms': 20000, 'trials': [case['trial']]}
    verify_case(good, 0, case['profile'], m['patch_sha256'], m)
    changes = {
        'wrong_identity': lambda d: d.update(identity='arbitrary-harness'),
        'wrong_patch': lambda d: d.update(patch_sha256='0'*64),
        'missing_trial': lambda d: d.update(trials=[]),
        'extra_trial': lambda d: d['trials'].append(copy.deepcopy(d['trials'][0])),
        'missing_assertion': lambda d: d['trials'][0]['last']['progress'].pop(),
        'extra_assertion': lambda d: d['trials'][0]['last']['progress'].append(d['trials'][0]['last']['progress'][0]),
        'failed_assertion': lambda d: d['trials'][0]['last']['progress'][0].update({'pass': False}),
        'wrong_order': lambda d: d['trials'][0]['last']['progress'].reverse(),
        'skipped_trial': lambda d: d['trials'][0].update(status='SKIPPED'),
        'flaky_trial': lambda d: d['trials'][0].update(status='FLAKY'),
        'not_run_trial': lambda d: d['trials'][0].update(status='NOT_RUN'),
        'unknown_trial': lambda d: d['trials'][0].update(status='UNKNOWN'),
        'deadline_extension': lambda d: d.update(deadline_ms=40000),
        'timeout': lambda d: d['trials'][0].update(smoke_ms=20001),
        'page_incomplete': lambda d: d['trials'][0]['last'].update(result='pending'),
        'no_timer': lambda d: d['trials'][0]['last'].update(readiness=[]),
        'fake_clock': lambda d: [x.update(value=0) for x in d['trials'][0]['last']['readiness'] if x['label']=='real-clock-callback'],
        'page_exception': lambda d: d['trials'][0]['events'].append({'method':'Runtime.exceptionThrown'}),
        'network_failure': lambda d: d['trials'][0]['events'].append({'method':'Network.loadingFailed'}),
        'missing_resources': lambda d: d['trials'][0].update(after={}),
        'nonzero_exit': lambda d: None,
    }
    passed = []
    for name, mutate in changes.items():
        data = copy.deepcopy(good)
        mutate(data)
        try:
            verify_case(data, 1 if name == 'nonzero_exit' else 0, case['profile'], m['patch_sha256'], m)
        except (ValueError, KeyError, TypeError):
            passed.append(name)
        else:
            raise ValueError('False PASS: ' + name)
    return {'status': 'PASS', 'valid_control': 'PASS', 'rejected_negative_cases': passed, 'count': len(passed)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'negative', 'verify', 'source'])
    parser.add_argument('--directory', type=Path, required=True)
    args = parser.parse_args()
    m = load_manifest()
    directory = args.directory.resolve()
    if args.action == 'prepare':
        prepare(directory, m)
    elif args.action == 'negative':
        save(directory / 'negative-tests.json', negative_tests(m))
    elif args.action == 'source':
        verify_source(directory / 'source', m, patched=True)
    else:
        executions = read_json(directory / 'executions.json')
        expected = [p['id'] for p in m['ci_profiles']]
        require([e['id'] for e in executions] == expected, 'Missing/extra/reordered CI IDs')
        results = []
        for execution, profile in zip(executions, m['ci_profiles']):
            data = read_json(directory / 'results' / (profile['id'] + '.json'))
            counts = verify_case(data, execution['exit_code'], profile['profile'], m['patch_sha256'], m)
            results.append({'id': profile['id'], **counts})
        verify_source(directory / 'source', m, patched=True)
        save(directory / 'gate-result.json', {'id': m['id'], 'status': 'PASS', 'expected_runs': len(expected), 'executed_runs': len(results), 'results': results})
    print(json.dumps({'action': args.action, 'status': 'PASS'}))


if __name__ == '__main__':
    main()
