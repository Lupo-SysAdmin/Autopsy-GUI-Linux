#!/usr/bin/env python3
"""Download pinned upstream artifacts; fail closed on checksum mismatch."""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    lock = json.loads((ROOT / 'versions.lock.json').read_text())
    cache = ROOT / '.cache'
    cache.mkdir(exist_ok=True)
    for key in sys.argv[1:] or lock:
        item = lock[key]
        target = cache / item['file']
        if not target.exists():
            part = target.with_suffix(target.suffix + '.part')
            subprocess.run(['curl', '--fail', '--location', '--retry', '3',
                            '--silent', '--show-error', '--proto', '=https',
                            item['url'], '-o', str(part)], check=True)
            if digest(part) != item['sha256']:
                part.unlink()
                raise SystemExit(f'Checksum mismatch / Hash incorrecto: {key}')
            part.replace(target)
        if digest(target) != item['sha256']:
            raise SystemExit(f'Checksum mismatch / Hash incorrecto: {target}')
        print(f'SHA256 OK: {target.name}', flush=True)


if __name__ == '__main__':
    main()
