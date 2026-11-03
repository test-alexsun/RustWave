"""Execute the approved CI matrix, keeping every exit and diagnostic artifact."""
import argparse
import json
import subprocess
import time
from pathlib import Path
from approved_browser_gate import load_manifest, prepare, save, negative_tests, verify_case, verify_source, require


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--image', default='rustwave-browser-v1:ci')
    parser.add_argument('--docker', default='docker')
    args = parser.parse_args()
    m = load_manifest()
    root = args.directory.resolve()
    prepare(root, m)
    records = []

    def command(name, argv, timeout=600, checked=True):
        started = time.monotonic()
        with (root / (name + '.stdout')).open('wb') as out, (root / (name + '.stderr')).open('wb') as err:
            try:
                code = subprocess.run(argv, stdout=out, stderr=err, timeout=timeout).returncode
            except subprocess.TimeoutExpired:
                code = 124
        records.append({'id': name, 'argv': argv, 'exit_code': code, 'duration_seconds': time.monotonic()-started})
        save(root / 'commands.json', records)
        if checked:
            require(code == 0, name + ' failed: ' + str(code))
        return code

    save(root / 'negative-tests.json', negative_tests(m))
    docker = [args.docker, 'run', '--rm']
    mounts = ['-v', f'{root / "source"}:/src:ro', '-v', f'{root / "deps"}:/src/frontend/node_modules',
              '-v', f'{root / "audit"}:/audit:ro', '-v', f'{root / "results"}:/evidence',
              '-v', f'{root / "original-smoke.tsx"}:/original-smoke.tsx:ro']
    env = ['-e', 'TZ=UTC', '-e', 'LC_ALL=C.UTF-8', '-w', '/src/frontend']
    command('versions', docker + ['--network', 'none', args.image, 'sh', '-c', 'bun --version && chromium --version'])
    versions = (root / 'versions.stdout').read_text()
    require(versions.splitlines()[0] == m['bun'] and ('Chromium ' + m['chromium'] + ' ') in versions, 'Tool versions drift')
    command('image', [args.docker, 'image', 'inspect', args.image])
    command('dependencies', docker + ['--cpus', '2', '--memory', '2000m', *mounts, *env, args.image, 'bun', 'install', '--frozen-lockfile'])
    command('assertions', docker + ['--network', 'none', *mounts, *env, args.image, 'bun', '/audit/approved_assertions.cjs'])
    executions = []
    outcomes = []
    for profile in m['ci_profiles']:
        name = profile['id']
        code = command(name, docker + ['--network', 'none', '--cpus', str(profile['cpus']), '--memory', str(profile['memory_mib'])+'m',
                                     *mounts, *env, '-e', 'AUDIT_PROFILE='+profile['profile'], '-e', 'AUDIT_RUN_ID='+name,
                                     args.image, 'bun', '/audit/patched_browser_runner.mjs'], timeout=300, checked=False)
        executions.append({'id': name, 'exit_code': code})
        save(root / 'executions.json', executions)
        try:
            data = json.loads((root / 'results' / (name+'.json')).read_text())
            outcome = verify_case(data, code, profile['profile'], m['patch_sha256'], m)
        except (OSError, ValueError, KeyError, TypeError) as error:
            outcome = {'status': 'FAIL', 'reason': str(error)}
        outcomes.append({'id': name, **outcome})
        print(json.dumps(outcomes[-1]), flush=True)
    verify_source(root / 'source', m, patched=True)
    result = {'id': m['id'], 'status': 'PASS' if all(r['status']=='PASS' for r in outcomes) else 'FAIL',
              'expected_runs': len(m['ci_profiles']), 'executed_runs': len(executions), 'results': outcomes}
    save(root / 'gate-result.json', result)
    require(result['status'] == 'PASS', 'Mandatory browser matrix failed')


if __name__ == '__main__':
    main()
