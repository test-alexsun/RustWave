// Compare every argument expression, expected value and order; no test transformation.
const fs = require('node:fs')
const parser = require('/src/frontend/node_modules/prettier/plugins/typescript.js').parsers.typescript
function assertions(file) {
    const code = fs.readFileSync(file, 'utf8')
    const found = []
    function visit(node) {
        if (!node || typeof node !== 'object') return
        if (node.type === 'CallExpression' && node.callee?.type === 'Identifier' && node.callee.name === 'assert') {
            found.push(node.arguments.map(a => code.slice(a.range[0], a.range[1]).replace(/\r\n/g, '\n')))
        }
        for (const [key, value] of Object.entries(node)) {
            if (['range', 'loc', 'tokens', 'comments'].includes(key)) continue
            if (Array.isArray(value)) value.forEach(visit)
            else if (value && typeof value === 'object') visit(value)
        }
    }
    visit(parser.parse(code, { filepath: file }))
    return found
}
const original = assertions('/original-smoke.tsx')
const patched = assertions('/src/frontend/tests/browser-smoke.tsx')
const manifest = JSON.parse(fs.readFileSync('/audit/browser-smoke-v1.identity.json', 'utf8'))
if (original.length !== 59 || JSON.stringify(original) !== JSON.stringify(patched)) throw Error('Assertion expression/order mismatch')
for (let i = 0; i < 59; i++) {
    if (original[i][1] !== "'" + manifest.assertions[i].message + "'") throw Error('Assertion identity mismatch: ' + i)
}
fs.writeFileSync('/evidence/assertion-equivalence.json', JSON.stringify({status:'PASS', count:59, identical_arguments_and_order:true, arguments:original}, null, 2)+'\n')
