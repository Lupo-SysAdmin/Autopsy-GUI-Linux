#!/usr/bin/env python3
"""Assemble the Linux binary redistribution without touching the host installation."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '4.23.1-4'


def main():
    os.chdir(ROOT)
    lock = json.loads(Path('versions.lock.json').read_text())
    stage = ROOT / 'build/package'
    if stage.exists():
        shutil.rmtree(stage)
    app = stage / 'opt/autopsy-gui'
    app.mkdir(parents=True)
    (stage / 'DEBIAN').mkdir()
    removed = []
    with zipfile.ZipFile(ROOT / '.cache' / lock['autopsy']['file']) as archive:
        for item in archive.infolist():
            relative = Path(item.filename).relative_to('autopsy-4.23.1')
            if '..' in relative.parts or relative.is_absolute():
                raise ValueError('Unsafe archive path')
            if item.is_dir():
                continue
            if relative.suffix.lower() in {'.exe', '.dll', '.pyd', '.pdb', '.chm', '.msi', '.lib'}:
                removed.append(str(relative))
                continue
            target = app / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(item))
            target.chmod(0o755 if (item.external_attr >> 16) & 0o111 else 0o644)
    # Upstream Java JAR already matches TSK 4.15.0. Replace only the native layer.
    shutil.copytree(ROOT / 'build/native', app / 'native', symlinks=True)
    # Upstream's loader reads JNI from NATIVELIBS inside this JAR, not java.library.path.
    jar = app / 'autopsy/modules/ext/sleuthkit-4.15.0.jar'
    with zipfile.ZipFile(jar, 'a', compression=zipfile.ZIP_DEFLATED) as archive:
        if any(n.upper().endswith(('.SF', '.RSA', '.DSA')) for n in archive.namelist()):
            raise RuntimeError('Refusing to modify a signed upstream JAR')
        archive.write(app / 'native/libtsk_jni.so', 'NATIVELIBS/amd64/linux/libtsk_jni.so')
        archive.writestr('META-INF/LINUX-INTEGRATION.txt',
                         'Modified by Lupo-SysAdmin: added Linux amd64 JNI built from TSK 4.15.0.\n'
                         'Original Java classes and upstream notices retained.\n')
    # The Java API is unchanged; ship the native library rebuilt from matching sources.
    subprocess.run(['python3', str(ROOT / 'scripts/verify-sevenzip.py')], check=True)
    shutil.copyfile(ROOT / 'build/sevenzip-build/sevenzipjbinding-Linux-amd64.jar',
                    app / 'autopsy/modules/ext/sevenzipjbinding-AllPlatforms.jar')
    runtime = app / 'runtime'
    runtime.mkdir()
    with tarfile.open(ROOT / '.cache' / lock['runtime']['file']) as archive:
        for member in archive.getmembers():
            parts = Path(member.name).parts[1:]
            if not parts:
                continue
            member.name = str(Path(*parts))
            archive.extract(member, runtime, filter='data')
    config = app / 'etc/autopsy.conf'
    text = '\n'.join(line for line in config.read_text().splitlines()
                     if not line.startswith('jdkhome=')) + '\n'
    config.write_text(text.replace('${DEFAULT_USERDIR_ROOT}/dev', '${DEFAULT_USERDIR_ROOT}/4.23')
                      .replace('${DEFAULT_CACHEDIR_ROOT}/dev', '${DEFAULT_CACHEDIR_ROOT}/4.23'))
    for path in [app / 'bin/autopsy', app / 'autopsy/markmckinnon/mm_artifact_parser_x64_linux', *(app / 'autopsy/solr/bin').glob('*'),
                 *(app / 'autopsy/markmckinnon').glob('export*'),
                 *(app / 'autopsy/markmckinnon').glob('parse*')]:
        if path.is_file():
            path.chmod(0o755)
    for source, dest in [
        ('packaging/autopsy-gui', 'usr/bin/autopsy-gui'),
        ('packaging/autopsy-gui.desktop', 'usr/share/applications/autopsy-gui.desktop'),
    ]:
        target = stage / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, target)
        target.chmod(0o755 if dest.startswith('usr/bin/') else 0o644)
    # Original Autopsy icon frames, converted to PNG with identical RGBA pixels.
    for icon in (ROOT / 'packaging/icons').glob('*/autopsy-gui.png'):
        target = stage / 'usr/share/icons/hicolor' / icon.parent.name / 'apps/autopsy-gui.png'
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(icon, target)
    doc = stage / 'usr/share/doc/autopsy-gui'
    doc.mkdir(parents=True)
    for name in ['LICENSE', 'NOTICE', 'README.md', 'README.es.md', 'THIRD_PARTY.md', 'versions.lock.json']:
        shutil.copyfile(ROOT / name, doc / name)
    shutil.copytree(ROOT / 'docs', doc / 'docs')
    shutil.copytree(ROOT / 'licensing', doc / 'licensing')
    shutil.copyfile(ROOT / 'third-party-sources.lock.json', doc / 'third-party-sources.lock.json')
    shutil.copyfile(ROOT / 'build/sevenzip-correspondence.json', doc / 'sevenzip-correspondence.json')
    # JAI's binary redistribution terms require the complete companion libraries.
    vendor = doc / 'vendor'
    vendor.mkdir()
    third_party = json.loads((ROOT / 'third-party-sources.lock.json').read_text())
    for item in third_party['redistributables']:
        payload = ROOT / '.cache/third-party' / item['file']
        if hashlib.sha256(payload.read_bytes()).hexdigest() != item['sha256']:
            raise RuntimeError('Unverified redistributable: ' + item['file'])
        shutil.copyfile(payload, vendor / item['file'])
    with zipfile.ZipFile(vendor / 'jai-1_1_3-lib.zip') as archive:
        shutil.copyfileobj(archive.open('jai-1_1_3/lib/jai_codec.jar'),
                           (app / 'autopsy/modules/ext/jai_codec-1.1.3.jar').open('wb'))

    subprocess.run(['python3', str(ROOT / 'scripts/inventory-jars.py'), str(app), str(doc / 'jar-inventory.json')], check=True)
    subprocess.run(['python3', str(ROOT / 'scripts/collect-notices.py'), str(app), str(doc / 'jar-inventory.json'), str(doc / 'embedded-notices.tar.gz')], check=True)
    (doc / 'copyright').write_text((ROOT / 'NOTICE').read_text() + '\n' +
                                 (ROOT / 'LICENSE').read_text() + '\n' +
                                 (ROOT / 'THIRD_PARTY.md').read_text())
    (doc / 'removed-windows-files.json').write_text(json.dumps(removed, indent=2) + '\n')
    shutil.copytree(ROOT / 'build/sleuthkit-4.15.0/licenses', doc / 'sleuthkit-licenses')
    for name in ['COPYING', 'README.md']:
        source = ROOT / 'build/sleuthkit-4.15.0' / name
        if source.exists():
            shutil.copyfile(source, doc / ('sleuthkit-' + name))
    info = {'package_version': VERSION, 'maintainer': 'Lupo-SysAdmin',
            'upstream': lock, 'build_os': Path('/etc/os-release').read_text(),
            'architecture': 'amd64', 'validation_record': '/usr/share/doc/autopsy-gui/docs/VALIDATION.md'}
    (app / 'build-info.json').write_text(json.dumps(info, indent=2) + '\n')
    (doc / 'build-packages.txt').write_text(subprocess.check_output(
        ['dpkg-query', '-W', '-f=${binary:Package}\t${Version}\n'], text=True))
    # Compute distro-specific native dependencies, including the private JVM.
    depdir = ROOT / 'build/deps'
    (depdir / 'debian').mkdir(parents=True, exist_ok=True)
    (depdir / 'debian/control').write_text('Source: autopsy-gui\nMaintainer: Lupo-SysAdmin <ascaniojan91@gmail.com>\n\nPackage: autopsy-gui\nArchitecture: amd64\nDescription: Autopsy Linux integration\n')
    elf = []
    for base in [app / 'native', runtime]:
        for path in base.rglob('*'):
            if path.is_file() and not path.is_symlink():
                with path.open('rb') as stream:
                    if stream.read(4) == b'\x7fELF':
                        elf.append(path)
    elf.append(app / 'autopsy/markmckinnon/mm_artifact_parser_x64_linux')
    # Also resolve native dependencies of the rebuilt SevenZip JNI.
    sevenzip_elf = ROOT / 'build/sevenzip-build/jbinding-cpp/lib7-Zip-JBinding.so'
    elf.append(sevenzip_elf)
    # Check that external shared libraries actually resolve in the builder.
    env = dict(os.environ, LD_LIBRARY_PATH=':'.join(map(str, [
        app / 'native', runtime / 'lib', runtime / 'lib/server'])))
    for path in elf:
        result = subprocess.run(['ldd', str(path)], capture_output=True, text=True, env=env)
        if 'not found' in result.stdout:
            raise RuntimeError(f'Unresolved native dependency: {path}\n{result.stdout}')
    args = ['dpkg-shlibdeps', '-O', '--ignore-missing-info', '-l' + str(app / 'native'),
            '-l' + str(runtime / 'lib'), '-l' + str(runtime / 'lib/server')]
    result = subprocess.run(args + ['-e' + str(p) for p in elf], cwd=depdir,
                            check=True, capture_output=True, text=True)
    (ROOT / 'build/shlibdeps.log').write_text(result.stderr)
    dependencies = result.stdout.strip().removeprefix('shlibs:Depends=')
    dep_list = dependencies.split(', ')
    for extra in ['bash', 'libgtk-3-0', 'libxtst6', 'libxi6', 'libxrender1', 'fonts-dejavu-core', 'photorec | testdisk (<< 7.2-1~)', 'procps', 'lsof']:
        if extra not in {d.split()[0] for d in dep_list}:
            dep_list.append(extra)
    dependencies = ', '.join(dep_list)
    control = stage / 'DEBIAN'
    control.mkdir(exist_ok=True)
    size = sum(p.stat().st_size for p in stage.rglob('*') if p.is_file()) // 1024
    (control / 'control').write_text(f'''Package: autopsy-gui
Version: {VERSION}
Architecture: amd64
Maintainer: Lupo-SysAdmin <ascaniojan91@gmail.com>
Section: utils
Priority: optional
Installed-Size: {size}
Depends: {dependencies}
Recommends: libgstreamer1.0-0, gstreamer1.0-plugins-base, gstreamer1.0-plugins-good, tesseract-ocr
Homepage: https://www.autopsy.com/
Description: Autopsy 4 desktop with independent Linux integration
 Unofficial Linux packaging and desktop integration by Lupo-SysAdmin.
 Autopsy and its original graphical interface are developed by upstream.
 Includes private Eclipse Temurin 21 runtime and The Sleuth Kit JNI.
 See the tested-platform matrix and module limitations before use.
''')
    for path in stage.rglob('*'):
        if not path.is_symlink():
            path.chmod(0o755 if path.is_dir() or path.stat().st_mode & 0o111 else 0o644)
    stage.chmod(0o755)
    (control / 'md5sums').write_text(''.join(
        f'{hashlib.md5(p.read_bytes()).hexdigest()}  {p.relative_to(stage)}\n'
        for p in sorted(stage.rglob('*'))
        if p.is_file() and not p.is_symlink() and 'DEBIAN' not in p.relative_to(stage).parts))
    (control / 'md5sums').chmod(0o644)
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    package = out / f'autopsy-gui_{VERSION}_amd64.deb'
    subprocess.run(['dpkg-deb', '--root-owner-group', '-Zxz', '-z3', '--build', str(stage), str(package)], check=True)
    subprocess.run(['python3', str(ROOT / 'scripts/bundle-third-party.py')], check=True)
    # Ship corresponding source archives beside the binary, not in Git history.
    for key in ['sleuthkit', 'runtime_source']:
        shutil.copyfile(ROOT / '.cache' / lock[key]['file'], out / lock[key]['file'])
    shutil.copyfile(ROOT / 'versions.lock.json', out / 'versions.lock.json')
    # Include build scripts and the upstream header supplement with every binary.
    with tarfile.open(out / f'autopsy-gui-integration-{VERSION}.tar.gz', 'w:gz') as archive:
        for path in sorted(ROOT.iterdir()):
            if path.name not in {'.git', '.cache', 'build', 'dist', '__pycache__'}:
                archive.add(path, arcname=f'autopsy-gui-{VERSION}/{path.name}',
                            filter=lambda item: None if '__pycache__' in item.name else item)
    print(package)


if __name__ == '__main__':
    main()
