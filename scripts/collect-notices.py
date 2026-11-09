#!/usr/bin/env python3
"""Make embedded JAR notices accessible without changing their original contents."""
import io
import json
from pathlib import Path
import sys
import tarfile
import zipfile
app, inventory, output = map(Path, sys.argv[1:])
records = json.loads(inventory.read_text())['jars']
with tarfile.open(output, 'w:gz') as bundle:
    for record in records:
        with zipfile.ZipFile(app / record['path']) as jar:
            for name in record['notices']:
                if Path(name).is_absolute() or '..' in Path(name).parts:
                    raise ValueError('Unsafe embedded notice path')
                data = jar.read(name)
                entry = tarfile.TarInfo(record['path'] + '/' + name)
                entry.size = len(data)
                entry.mode = 0o644
                bundle.addfile(entry, io.BytesIO(data))
print('Embedded notices collected without modifying their text.')
