"""Review preserved Stage01 evidence; never rerun Go tests or benchmarks."""
import argparse
import json
from pathlib import Path
from approved_browser_gate import ROOT, load_manifest, read_json, require, save, verify_case, verify_source
from gaps_report import outcomes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ci-directory', type=Path)
    parser.add_argument('--ci-metadata', type=Path)
    args = parser.parse_args()
    audit = ROOT / 'docs/audit'
    raw = ROOT / 'docs/benchmarks/raw'
    m = load_manifest()
    source_count = verify_source(raw / 'source-lf', m)
    expected = {x['id'] for x in read_json(audit / 'go-test-manifest.json')}
    require(len(expected) == 128, 'Go manifest denominator changed')
    full = read_json(audit / 'go-test-results.json')
    coverage = read_json(audit / 'supplementary-coverage.json')
    go = {}
    for mode in ('sqlite', 'postgres'):
        require(set(full[mode]['top']) == expected, 'Full suite missing/unexpected ID')
        supplements = {}
        for file in [raw/'gaps01'/f'schema-{mode}.stdout', raw/'gaps01'/f'migration-{mode}.stdout', raw/'gaps01/native'/f'native-{mode}.jsonl']:
            results = outcomes(file)
            require(results and all(v=='PASS' for v in results.values()), 'Supplement failed/skipped')
            supplements.update(results)
        rows = [r for r in coverage if r['mode'] == mode]
        require({r['id'] for r in rows if r['kind']=='top'} == expected, 'Coverage manifest missing ID')
        for row in rows:
            original = full[mode][row['kind']][row['id']]
            require(original == row['full_suite'], 'Historical outcome changed')
            cross_context = original=='SKIPPED' and row['id'].endswith('/postgres') and full['postgres']['nested'].get(row['id'])=='PASS'
            require(original=='PASS' or supplements.get(row['id'])=='PASS' or cross_context, 'Uncovered Go ID: '+row['id'])
            require(row['effective']=='PASS', 'Effective execution missing')
        go[mode] = {'expected':128, 'effective_pass':128, 'observed_child_pass':len([r for r in rows if r['kind']=='nested']), 'historical_counts':full[mode]['counts']}
    commands = {r['name']:r for f in [raw/'commands.json', raw/'extra/commands.json'] for r in read_json(f)}
    required_commands = ['lf-go-fmt-gate','lf-go-fmt-diff','lf-go-vet','lf-go-build','lf-frontend-check',
                         'lf-frontend-typecheck','lf-frontend-build','lf-installer','lf-response-headers',
                         'lf-contract-export','lf-contract-probes','lf-branding','lf-image-build','lf-image-inspect']
    require(all(commands[k]['exit']==0 for k in required_commands), 'Mandatory command missing/failed')
    units = read_json(audit/'frontend-test-manifest.json')
    log = (raw/'lf-frontend-test.stderr').read_text(encoding='utf-8')
    require(len(units)==24 and commands['lf-frontend-test']['exit']==0 and log.count('(pass) ')==24, 'Unit test accounting')
    require(all(t['name'] in log for t in units), 'Unit ID missing in actual output')
    baseline = read_json(raw/'baseline.json')
    for mode in ('sqlite','postgres'):
        require(len(baseline['modes'][mode])==3, 'Missing baseline trial')
        for trial in baseline['modes'][mode]:
            require(all(trial[k]>0 for k in ['startup_seconds','idle_seconds','backend_rss_bytes']), 'Missing baseline measurement')
            require('backend_cpu_percent' in trial and 'database' in trial, 'Missing separate backend/DB measurements')
        require(baseline['metrics_disabled'][mode]['pass'], 'Disabled metrics probe')
    counts = read_json(audit/'counts.json')
    require((counts['feature_items'],counts['api_operations'],counts['frontend_calls'])==(304,248,221), 'Inventory artifact mismatch')
    qualification = read_json(audit/'browser-patch-v1-results.json')
    require(len(qualification['trials'])==20, 'Missing browser qualification run')
    for t in qualification['trials']:
        verify_case({'identity':m['id'],'patch_sha256':m['tested_context_patch_sha256'],'profile':t['profile'],'deadline_ms':20000,'trials':[t['trial']]},t['command']['exit'],t['profile'],m['tested_context_patch_sha256'],m)
    ci = {'status':'NOT_RUN'}
    if args.ci_directory and args.ci_metadata:
        meta = read_json(args.ci_metadata)
        require(meta['conclusion']=='success' and meta['status']=='completed', 'CI did not succeed')
        directory = args.ci_directory
        executions = read_json(directory/'executions.json')
        require([e['id'] for e in executions] == [p['id'] for p in m['ci_profiles']], 'CI expected/executed mismatch')
        for execution, profile in zip(executions,m['ci_profiles']):
            verify_case(read_json(directory/'results'/(profile['id']+'.json')),execution['exit_code'],profile['profile'],m['patch_sha256'],m)
        equivalent = read_json(directory/'results/assertion-equivalence.json')
        require(equivalent['status']=='PASS' and equivalent['count']==59, 'CI assertion equivalence missing')
        require(equivalent['arguments']==read_json(audit/'browser-v1-formal-review.json')['assertions']['arguments'], 'CI assertion expression drift')
        negative = read_json(directory/'negative-tests.json')
        require(negative['status']=='PASS' and negative['count']==21, 'CI negative checks missing')
        integrity = read_json(directory/'integrity.json')
        require(integrity['patched_tsx_sha256']==m['tested_tsx_sha256'] and integrity['runner_sha256']==m['tested_runner_sha256'], 'CI execution bytes differ')
        ci = {'status':'PASS','expected':4,'executed':4,'passed':4,'failed':0,'skipped':0,'not_run':0,'flaky':0,'run':meta}
    result = {'source_blobs':source_count,'inventory_items':304,'http_ws_operations':248,'frontend_callsites':221,
              'go':go,'command_checks':{'expected':14,'passed':14,'ids':required_commands},'frontend_unit':{'expected':24,'passed':24},
              'baseline_trials':{'expected':6,'passed':6},'browser_qualification':{'expected':20,'passed':20,'assertions_per_run':59},
              'browser_ci':ci,'historical_original':'HISTORICAL_FLAKY','rust_parity':'NOT_TESTED',
              'local_evidence_review':'PASS','stage':'PASS' if ci['status']=='PASS' else 'PARTIAL',
              'blockers':[] if ci['status']=='PASS' else ['Mandatory browser CI evidence pending']}
    save(audit/'stage01-final-review.json',result)
    print(json.dumps({'local_evidence_review':result['local_evidence_review'],'ci':ci['status'],'stage':result['stage']}))


if __name__ == '__main__':
    main()
