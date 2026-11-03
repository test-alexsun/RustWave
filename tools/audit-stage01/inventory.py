"""Source inventories; no generated row claims behavioral compatibility."""
from pathlib import Path
import collections
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs'
OUT = DOC / 'audit'
OUT.mkdir(exist_ok=True)
SHA = 'd709bad01dc0ceacb20012a3afdf528eddfd061f'


def read(p):
    return source_bytes(p).decode('utf-8')


def source_bytes(p):
    # Analyse pinned blob bytes, not Git-for-Windows checkout conversions.
    try:
        relative=p.relative_to(ROOT)
    except ValueError:
        return p.read_bytes()
    pinned=ROOT/'docs/benchmarks/raw/source-lf'/relative
    if relative.parts[0] not in ('docs','tools') and pinned.is_file():
        return pinned.read_bytes()
    return p.read_bytes()


def loc(p, text, pos):
    return f'{p.relative_to(ROOT).as_posix()}:{text.count(chr(10), 0, pos)+1}'


def table(headers, rows):
    def escape(v):
        return str(v).replace('|', '&#124;').replace('\n', '<br>')
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---']*len(headers))+' |'] +
                     ['| ' + ' | '.join(escape(v) for v in row)+' |' for row in rows])+'\n'


def write(p, title, intro, headers, rows):
    p.write_text(f'# {title}\n\nSource: `{SHA}`.\n\n{intro}\n\n'+table(headers, rows), encoding='utf-8')


def main():
    commands = json.loads(read(ROOT/'backend-go/internal/contracts/commands.json'))['commands']
    cm = {c['name']: c for c in commands}
    api = json.loads(read(ROOT/'backend-go/internal/contracts/openapi.json'))
    routes, tests, funcs, sources, packages = [], [], [], [], {}
    models = dict(re.findall(r'func \((\w+)\) TableName\(\) string\s*{\s*return "([^"]+)"', read(ROOT/'backend-go/internal/database/models.go')))
    # schemaModels also includes these conventional GORM names (verified in 001_initial.sql).
    models.update(AuthChallenge='auth_challenges', Job='jobs', ScheduledExecution='scheduled_executions')
    for p in sorted((ROOT/'backend-go').rglob('*.go')):
        s = read(p)
        package = p.parent.relative_to(ROOT/'backend-go').as_posix()
        sources.append((p.relative_to(ROOT).as_posix(), hashlib.sha256(source_bytes(p)).hexdigest()))
        if p.name.endswith('_test.go'):
            for m in re.finditer(r'^func (Test\w+)\(t \*testing.T\)', s, re.M):
                tests.append(dict(id='gowave/'+package+'/'+m[1], package='gowave/'+package, name=m[1], source=loc(p,s,m.start())))
            continue
        info = packages.setdefault(package, dict(files=[], deps=set(), models=set(), funcs=[]))
        info['files'].append(p.relative_to(ROOT).as_posix())
        info['deps'].update(re.findall(r'^\s*(?:\w+ )?"((?:github.com|golang.org|gorm.io|modernc.org|filippo.io|gopkg.in)[^"]+)"',s,re.M))
        info['models'].update(models[x] for x in re.findall(r'database\.(\w+)',s) if x in models)
        for m in re.finditer(r'^func (?:\(([^)]+)\) )?(\w+)\(',s,re.M):
            item=[package, m[2], m[1] or '',loc(p,s,m.start())]
            funcs.append(item)
            info['funcs'].append(m[2])
        # Production Chi registrations are all literal method calls in three files.
        for m in re.finditer(r'\b(r|protected)\.(Get|Post|Patch|Put|Delete|Head|Options)\("([^"]+)",\s*([^\n]+)\)',s):
            path=m[3]
            if path=='/*':
                continue
            auth='Bearer JWT/API token + scopes/AdminOnly'
            if p.name=='server.go' and m[1]=='r': auth='public (handler checks); SSH uses ticket + protocol'
            if p.name=='tools.go': auth='OTT -> rw-tools cookie; admin + same-origin mutation'
            handler=m[4].strip()
            routes.append(dict(method=m[2].upper(), path=path, handler=handler, source=loc(p,s,m.start()), auth=auth))
    routes.sort(key=lambda r:(r['path'],r['method']))
    for i,r in enumerate(routes,1): r['id']=f'API-{i:03}'
    assert len({(r['method'],r['path']) for r in routes})==len(routes), 'duplicate routes'
    write(OUT/'HTTP_ROUTES.md','HTTP / WebSocket route inventory',
          f'{len(routes)} explicit main-listener method/path operations; includes WS upgrade GET and 2 HEAD. Static GET/HEAD wildcard and metrics listener GET /metrics, GET /health are counted separately. CORS preflight is middleware, not an extra registered operation. No Rust implementation.',
          ['ID','Method','Path','Handler','Registration','Authentication'],
          [[r[k] for k in ('id','method','path','handler','source','auth')] for r in routes])
    write(OUT/'GO_SYMBOLS.md','Go production symbol index','Discovery aid, not a business-feature count. Includes every production Go function/method declaration.',
          ['Package','Function','Receiver','Source'],funcs)
    write(OUT/'DATABASE_TABLES.md','Database model mapping','37 explicit TableName methods + 3 default GORM names from schemaModels; additionally gowave_migrations. SQL migrations are authoritative. Some join models are referenced via associations rather than direct package expressions.',
          ['Go model','SQL table'],sorted(models.items()))
    write(OUT/'SOURCE_FILES.md','Go source checksums','SHA-256 of LF archive files, verified against pinned Git blob hashes before execution. Windows checkout and the first archive have CRLF conversions; see ARCHIVE_INTEGRITY.md.', ['File','SHA-256'],sources)
    (OUT/'go-test-manifest.json').write_text(json.dumps(tests,indent=2)+'\n',encoding='utf-8')
    (OUT/'routes.json').write_text(json.dumps(routes,indent=2)+'\n',encoding='utf-8')
    package_rows=[]
    for pkg,info in packages.items():
        testnames=[t['name'] for t in tests if t['package']=='gowave/'+pkg]
        package_rows.append([pkg, ', '.join(info['files']), ', '.join(sorted(info['models'])) or 'No direct model reference; see called services / SQL', ', '.join(sorted(info['deps'])) or 'standard library / internal packages', ', '.join(testnames) or 'No colocated top-level tests'])
    write(OUT/'GO_PACKAGES.md','Go package and dependency coverage',f'{len(packages)} production directories. Model column is direct-reference evidence, not an exhaustive transitive table-access claim.',
          ['Package','Source files','Direct DB tables','External imports','Colocated tests'],package_rows)
    # All hook endpoint declarations plus direct transport callsites outside factories.
    tsfiles={p:read(p) for p in sorted((ROOT/'frontend/src').rglob('*')) if p.suffix in ('.ts','.tsx') and '.test.' not in p.name}
    calls=[]
    for p,s in tsfiles.items():
        if '/tsq-helpers/' in p.as_posix(): continue
        pattern=r'\bendpoint:\s*([^,\n]+)|\b(?:instance|axios)\s*\.(get|post|put|patch|delete)(?:<[^;]+?>)?\s*\(|\bfetch\(|new WebSocket\('
        for m in re.finditer(pattern,s):
            if m[1] and not ('.TSQ_url' in m[1] or m[1].startswith(("'", '"', '`'))):
                continue  # Type declarations are not callsites.
            # Ignore the editor object named instance; it has no matching calls.
            exports=list(re.finditer(r'export (?:const|function) (\w+)',s[:m.start()]))
            hook=exports[-1][1] if exports else p.stem
            next_export=s.find('\nexport ',m.end())
            block=s[m.start():next_export if next_export>=0 else len(s)]
            expr=m[1] or s[m.start():m.start()+350].split('\n\n')[0]
            cmdmatch=re.search(r'(\w+Command)\.(?:TSQ_url|url)',expr)
            c=cm.get(cmdmatch[1]) if cmdmatch else None
            schema=re.findall(r'(?:responseSchema|bodySchema|requestSchema|requestQuerySchema|routeParamsSchema):\s*([^,\n]+)',block)
            consumers=[q.relative_to(ROOT).as_posix() for q,t in tsfiles.items() if q!=p and re.search(r'\b'+re.escape(hook)+r'\b',t) and '/hooks/' not in q.as_posix()]
            actual_method=re.search(r'requestMethod:\s*[\'\"](\w+)',block)
            factory=s[exports[-1].start():m.start()] if exports else ''
            method=(m[2] or (actual_method[1] if actual_method else '') or ('GET' if 'createGet' in factory else '') or (c['method'] if c else 'manual')).upper()
            calls.append(dict(id=f'FE-{len(calls)+1:03}',source=loc(p,s,m.start()),hook=hook,expression=expr,
                              command=c['name'] if c else '',method=method,path=c['path'] if c else '',schemas=schema,consumers=consumers))
    (OUT/'frontend-calls.json').write_text(json.dumps(calls,indent=2)+'\n',encoding='utf-8')
    write(DOC/'FRONTEND_API_SHAPE_MATRIX.md','Frontend API callsite / shape matrix',
          f'{len(calls)} callsites: factory declarations and direct axios/fetch/WebSocket transports; external asset fetches retained and labelled in manual supplement. Shapes below refer to exact pinned command schemas, expanded in [contract shapes](audit/CONTRACT_SHAPES.md). Direct custom transports are explained in [manual map](audit/FRONTEND_CUSTOM.md). Factory implementation: shared/api/tsq-helpers; Authorization/browser header and 401 logout: shared/api/axios.ts. Every row: Go fixture NOT_CAPTURED, Rust fixture NOT_STARTED, SQLite/PG differential NOT_TESTED; future integration IDs equal FE IDs. Consumers are direct identifier references, not a claim that every hook is reachable from a page. UI route mapping is in the manual supplement.',
          ['ID','Callsite / hook','Actual method / contract path','Expression','Schema references','Direct UI consumers','SQLite / PG / Rust'],
          [[c['id'],c['source']+' '+c['hook'],c['method']+' '+c['path'],c['expression'],', '.join(c['schemas']),'<br>'.join(c['consumers']) or 'No direct consumer found; inspect re-exports / dynamic callers','NOT_TESTED / NOT_TESTED / NOT_STARTED'] for c in calls])
    # Full, lossless operation schemas keep nested fields, enums, nullability and required sets.
    text=f'# Pinned frontend contract request/response shapes\n\nSource `{SHA}`; embedded contract 3.4.15. These are schema expectations, not observed response fixtures. Actual frontend schema choices and custom paths are in the callsite matrix. Global OpenAPI security is not authoritative for public routes. No nullable/optional fields are stripped.\n'
    for c in commands:
        path=re.sub(r':(\w+)',r'{\1}',c['path'])
        op=api['paths'].get(path,{}).get(c['method'].lower())
        text+=f'\n## {c["name"]}\n\n`{c["method"]} {c["path"]}`; scope `{c.get("scope", "")}`.\n\n'
        text+='```json\n'+json.dumps(op,ensure_ascii=False,indent=2)+'\n```\n' if op else 'No embedded OpenAPI operation: BLOCKED shape reference.\n'
    (OUT/'CONTRACT_SHAPES.md').write_text(text,encoding='utf-8')
    fixtures=[]
    for p in sorted((ROOT/'backend-go').rglob('*')):
        if p.is_file() and ('testdata' in p.parts or ('fixture' in p.name or 'golden' in p.name)):
            data=source_bytes(p)
            fixtures.append([p.relative_to(ROOT).as_posix(),len(data),hashlib.sha256(data).hexdigest()])
    write(OUT/'FIXTURES.md','Committed fixture inventory','No fixtures regenerated. See scripts/subscription-diff for upstream generation dependencies.', ['Path','Bytes','SHA-256'],fixtures)
    counts=dict(api_operations=len(routes),go_tests=len(tests),go_symbols=len(funcs),go_packages=len(packages),frontend_calls=len(calls),contract_commands=len(commands),fixtures=len(fixtures),models=len(models))
    (OUT/'counts.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(counts))


if __name__=='__main__': main()
