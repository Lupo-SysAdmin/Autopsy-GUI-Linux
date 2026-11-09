#!/usr/bin/env python3
"""Require exact correspondence of the rebuilt SevenZip API to the official ZIP."""
import hashlib
import io
import json
from pathlib import Path
import zipfile
root = Path(__file__).resolve().parents[1]
lock = json.loads((root / 'versions.lock.json').read_text())
with zipfile.ZipFile(root / '.cache' / lock['autopsy']['file']) as upstream:
    names = [n for n in upstream.namelist() if n.endswith('/sevenzipjbinding.jar')]
    if len(names) != 1:
        raise RuntimeError(f'Unexpected SevenZip API paths: {names}')
    original = zipfile.ZipFile(io.BytesIO(upstream.read(names[0])))
    with zipfile.ZipFile(root / 'build/sevenzip-build/jbinding-java/sevenzipjbinding.jar') as rebuilt:
        classes = {n for n in original.namelist() if n.endswith('.class')}
        assert classes == {n for n in rebuilt.namelist() if n.endswith('.class')}
        assert all(original.read(n) == rebuilt.read(n) for n in classes)
        result = {'source': lock['sevenzip_source'], 'identical_java_classes': len(classes),
                  'native_sha256': hashlib.sha256((root / 'build/sevenzip-build/sevenzipjbinding-Linux-amd64.jar').read_bytes()).hexdigest()}
(root / 'build/sevenzip-correspondence.json').write_text(json.dumps(result, indent=2) + '\n')
print(f'SevenZip: {len(classes)} Java classes match upstream byte for byte.')
