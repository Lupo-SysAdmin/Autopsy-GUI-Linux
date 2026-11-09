#!/usr/bin/env python3
"""Exercise the real installed Swing UI under Xvfb; synthetic evidence only."""
import base64
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/gui-regression'
OUT.mkdir(parents=True, exist_ok=False)  # Never reuse stale test results.
PROBE = OUT / 'probe'
PROBE.mkdir()
ENV = dict(os.environ, XDG_DATA_HOME=str(OUT / 'data'), XDG_CACHE_HOME=str(OUT / 'cache'))
subprocess.run(['javac', '--release', '21', '-d', str(OUT), str(ROOT / 'tests/GuiProbe.java')], check=True)
(OUT / 'manifest').write_text('Premain-Class: GuiProbe\n')
subprocess.run(['jar', 'cfm', str(OUT / 'probe.jar'), str(OUT / 'manifest'), '-C', str(OUT), 'GuiProbe.class'], check=True)

def tree():
    if (PROBE / 'error').exists():
        raise RuntimeError((PROBE / 'error').read_text())
    try:
        return json.loads((PROBE / 'tree.json').read_text())
    except FileNotFoundError:
        return []

def wait(predicate, description, timeout=90):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = predicate()
        if result:
            return result
        if process.poll() is not None:
            raise RuntimeError('Autopsy exited: ' + str(process.returncode))
        time.sleep(.5)
    raise TimeoutError(description)

def find(text, suffix=''):
    return next((c for c in tree() if c['text'] == text and c['class'].endswith(suffix) and c['enabled']), None)

def send(verb, control, value=None):
    wait(lambda: not (PROBE / 'command').exists(), 'probe command consumed')
    temp = PROBE / 'command.tmp'
    temp.write_text(verb + '\t' + str(control['id']) + ('' if value is None else '\t' + str(value)))
    temp.replace(PROBE / 'command')
    wait(lambda: not (PROBE / 'command').exists(), 'probe command applied')
    time.sleep(1.2)

def click(text):
    send('click', wait(lambda: find(text, 'JButton'), text))

def fill(control, value):
    send('text', control, base64.b64encode(value.encode()).decode())

def fields():
    return [c for c in tree() if c['class'].endswith('JTextField') and c['enabled']]

def shot(name):
    subprocess.run(['import', '-window', 'root', str(OUT / name)], check=True)

console = (OUT / 'console.log').open('w')
process = subprocess.Popen(['autopsy-gui', '--nosplash', '-J-javaagent:' + str(OUT / 'probe.jar') + '=' + str(PROBE)],
                           env=ENV, stdout=console, stderr=subprocess.STDOUT, start_new_session=True)
try:
    wait(lambda: find('OK') or find('New Case'), 'first launch', 180)
    if find('OK'):
        click('OK')
    label = wait(lambda: find('New Case'), 'welcome')
    send('click', next(c for c in tree() if c['parent'] == label['parent'] and c['class'].endswith('JButton')))
    wait(lambda: len(fields()) == 3, 'new case fields')
    fill(fields()[1], 'QA Linux GUI')
    base = OUT / 'Casos de prueba á'
    base.mkdir()
    fill(fields()[2], str(base))
    click('Next >')
    click('Finish')
    wait(lambda: find('Select Host', 'JLabel'), 'host wizard', 180)
    click('Next >')
    wait(lambda: find('Select Data Source Type', 'JLabel'), 'source type')
    click('Next >')
    wait(lambda: fields(), 'image path')
    fill(fields()[0], str(ROOT / 'build/fixtures with spaces/ext4.raw'))
    click('Next >')
    table = wait(lambda: next((c for c in tree() if c['class'].endswith('JTable') and any('Keyword Search' in i for i in c['items'])), None), 'ingest modules')
    for module in ['Android Analyzer (aLEAPP)', 'iOS Analyzer (iLEAPP)', 'YARA Analyzer']:
        assert next(row for row in table['items'] if row.endswith(' | ' + module)).startswith('false |'), module
    row = next(i for i, value in enumerate(table['items']) if value.endswith(' | Keyword Search'))
    send('table', table, f'{row},0,true')
    click('Next >')
    wait(lambda: find('Finish'), 'data source added', 180)
    assert not any('ingest cancelled' in (c['text'] or '') for c in tree())
    click('Finish')
    case = base / 'QA Linux GUI'
    log = case / 'Log/autopsy.log.0'
    wait(lambda: log.exists() and re.search(r'Ingest job \d+ completed', log.read_text()), 'ingest completion', 240)
    assert 'SEVERE:' not in log.read_text(), 'Ingest logged a severe error; inspect case log'
    listeners = [line.split()[1] for name in ['tcp', 'tcp6'] for line in Path('/proc/net', name).read_text().splitlines()[1:] if line.split()[3] == '0A' and line.split()[1].endswith(':5AC0')]
    allowed = {'0100007F:5AC0', '0000000000000000FFFF00000100007F:5AC0'}
    assert listeners and all(address in allowed for address in listeners), f'Solr must listen only on localhost: {listeners}'
    send('mouse', wait(lambda: find('Keyword Search', 'JButton'), 'keyword toolbar'))
    wait(lambda: find('Search', 'JButton') and fields(), 'keyword search popup')
    fill(fields()[0], 'fixture')
    click('Search')
    wait(lambda: any(any(row.startswith('evidence.txt') for row in c['items']) for c in tree()), 'expected keyword hit', 120)
    shot('keyword-hit.png')
    click('Generate Report')
    reports = wait(lambda: next((c for c in tree() if c['class'].endswith('JList') and any('HTMLReport' in i for i in c['items'])), None), 'report formats')
    send('listclick', reports, next(i for i, row in enumerate(reports['items']) if 'HTMLReport' in row))
    click('Next >')
    click('Next')
    click('Finish')
    wait(lambda: list((case / 'Reports').rglob('Keyword_Hits.html')), 'HTML report', 120)
    report = next((case / 'Reports').rglob('Keyword_Hits.html'))
    wait(lambda: 'evidence.txt' in report.read_text() and 'fixture' in report.read_text(), 'expected report contents')
    shot('report.png')
    platform_log = OUT / 'data/autopsy-gui/var/log/messages.log'
    assert platform_log.is_file(), 'Missing platform startup log'
    assert not re.search(r'^SEVERE', platform_log.read_text(), re.MULTILINE), 'Severe startup/platform error; inspect messages.log'
    (OUT / 'PASS').write_text('GUI case creation, Linux module defaults, ingest, keyword hit, HTML report: PASS\n')
    print((OUT / 'PASS').read_text(), flush=True)
finally:
    try:
        shot('final.png')
        (OUT / 'final-tree.json').write_text(json.dumps(tree(), indent=2))
    finally:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        console.close()
