#!/usr/bin/env python3
"""Check archive metadata and payload, without installing it."""
import hashlib
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
package = root / 'dist/autopsy-gui_4.23.1-3_amd64.deb'
assert subprocess.check_output(['dpkg-deb', '-f', str(package), 'Package'], text=True).strip() == 'autopsy-gui'
assert subprocess.check_output(['dpkg-deb', '-f', str(package), 'Architecture'], text=True).strip() == 'amd64'
listing = subprocess.check_output(['dpkg-deb', '-c', str(package)], text=True)
for required in ['usr/bin/autopsy-gui', 'applications/autopsy-gui.desktop', 'runtime/bin/java', 'native/libtsk_jni.so', 'doc/autopsy-gui/NOTICE']:
    assert required in listing, required
assert 'usr/bin/autopsy\n' not in listing
assert '/home/lupo/' not in listing
assert all('root/root' in line for line in listing.splitlines())
assert all(line[5] != 'w' and line[8] != 'w' for line in listing.splitlines() if not line.startswith('l'))
assert not any(line.split()[-1].lower().endswith(('.exe', '.dll', '.pyd')) for line in listing.splitlines())
lines = []
for path in sorted((root / 'dist').iterdir()):
    if path.is_file() and path.name != 'SHA256SUMS':
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        lines.append(f'{digest.hexdigest()}  {path.name}\n')
(root / 'dist/SHA256SUMS').write_text(''.join(lines))
print('Package structure and checksums OK / Estructura y hashes correctos')
