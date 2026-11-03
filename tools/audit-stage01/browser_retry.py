"""Retry only the failed browser check; preserve all prior evidence."""
import json
import browser as b


def main():
    h = b.h
    h.records = json.loads((h.RAW / 'commands.json').read_text())
    name = 'lf-browser-idle'
    if any(r['name'] == name for r in h.records):
        raise SystemExit('Retry evidence already exists; refusing to overwrite it.')
    base = ['run', '--rm', '--network', 'none', '--memory', '2000m', '--cpus', '2',
            '-v', str(b.SRC) + ':/src',
            '-v', str(b.ORIGINAL_RAW / 'source/frontend/node_modules') + ':/src/frontend/node_modules',
            '-w', '/src/frontend', b.IMAGE]
    h.run(name, [h.DOCKER, *base, 'bun', 'run', 'test:browser'], timeout=300)


if __name__ == '__main__':
    main()
