// Static equivalence of all original assertion expressions and expected values.
const fs = require('node:fs')
const path = require('node:path')
const root = path.resolve(__dirname, '../..')
const raw = path.join(root, 'docs/benchmarks/raw')
const parser = require(path.join(raw, 'source/frontend/node_modules/prettier/plugins/typescript.js')).parsers.typescript
function assertions(file) {
    const code = fs.readFileSync(file, 'utf8')
    const source = parser.parse(code, { filepath: file })
    const found = []
    function visit(node) {
        if (!node || typeof node !== 'object') return
        if (node.type === 'CallExpression' && node.callee?.type === 'Identifier' && node.callee.name === 'assert') {
            found.push(node.arguments.map(a => code.slice(a.range[0], a.range[1]).replace(/\r\n/g, '\n')))
        }
        for (const [key, value] of Object.entries(node)) {
            if (['range','loc','tokens','comments'].includes(key)) continue
            if (Array.isArray(value)) value.forEach(visit)
            else if (value && typeof value === 'object') visit(value)
        }
    }
    visit(source)
    return found
}
const old = assertions(path.join(raw, 'source-lf/frontend/tests/browser-smoke.tsx'))
const patched = assertions(path.join(raw, 'patched-v1/source/frontend/tests/browser-smoke.tsx'))

if (old.length !== 59 || JSON.stringify(old) !== JSON.stringify(patched)) throw Error('Assertion AST mismatch')
const result = { status: 'PASS', assertion_calls: old.length, identical_arguments_and_order: true, normalization: "CRLF to LF in source text only; four multiline expression whitespace breaks, no changed literal values" }
fs.writeFileSync(path.join(root, 'docs/audit/browser-patch-v1-assertion-check.json'), JSON.stringify(result, null, 2)+'\n')
console.log(JSON.stringify(result))
