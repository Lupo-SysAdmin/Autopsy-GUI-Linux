#!/usr/bin/env python3
"""Record bundled JAR identities and embedded legal evidence, without assuming a license."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('application', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
entries = []
for path in sorted(args.application.rglob('*.jar')):
    item = {'path': str(path.relative_to(args.application)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'notices': [], 'coordinates': [], 'declared_licenses': []}
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if re.match(r'^(LICENSE|NOTICE|COPYING|COPYRIGHT)([.\-_].*)?$', Path(name).name, re.I):
                item['notices'].append(name)
            if name.startswith('META-INF/maven/') and name.endswith('/pom.properties'):
                item['coordinates'].append(archive.read(name).decode('utf-8', errors='replace'))
            if name.startswith('META-INF/maven/') and name.endswith('/pom.xml'):
                try:
                    root = ET.fromstring(archive.read(name))
                    for element in root.iter():
                        element.tag = element.tag.rsplit('}', 1)[-1]
                    for license in root.findall('./licenses/license'):
                        item['declared_licenses'].append({child.tag: child.text for child in license})
                except ET.ParseError:
                    item.setdefault('unparsed_poms', []).append(name)
    entries.append(item)
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps({'scope': 'JAR metadata only; not a complete SBOM or redistribution clearance',
                                  'jars': entries}, indent=2) + '\n')
print(f'{len(entries)} JARs inventoried; license evidence is not a license conclusion')
