#!/usr/bin/env python3
"""Fetch pinned third-party source/redistributable archives and assemble release sources."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
from fetch import digest
ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch-only', action='store_true')
    args = parser.parse_args()
    lock = json.loads((ROOT / 'third-party-sources.lock.json').read_text())
    cache = ROOT / '.cache/third-party'
    cache.mkdir(parents=True, exist_ok=True)
    items = lock['sources'] + lock.get('redistributables', [])
    for item in items:
        name = item['file']
        if Path(name).name != name:
            raise ValueError(f'Unsafe filename: {name}')
        target = cache / name
        if not target.exists():
            part = target.with_suffix(target.suffix + '.part')
            subprocess.run(['curl', '--fail', '--location', '--retry', '3', '--silent',
                            '--show-error', '--proto', '=https', item['url'], '-o', str(part)], check=True)
            if digest(part) != item['sha256']:
                part.unlink()
                raise RuntimeError(f'Checksum mismatch: {name}')
            part.replace(target)
        if digest(target) != item['sha256']:
            raise RuntimeError(f'Checksum mismatch: {name}')
        print(f'SHA256 OK: {name}', flush=True)
    if args.fetch_only:
        return
    (ROOT / 'dist').mkdir(exist_ok=True)
    with tarfile.open(ROOT / 'dist/autopsy-third-party-sources-4.23.1.tar.gz', 'w:gz') as archive:
        archive.add(ROOT / 'third-party-sources.lock.json', arcname='third-party-sources/manifest.json')
        archive.add(ROOT / 'licensing', arcname='third-party-sources/licensing')
        for item in lock['sources']:
            archive.add(cache / item['file'], arcname='third-party-sources/' + item['file'])

if __name__ == '__main__':
    main()
