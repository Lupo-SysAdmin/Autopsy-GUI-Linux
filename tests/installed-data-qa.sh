#!/bin/bash
set -euo pipefail
app=/opt/autopsy-gui
classpath="$app/autopsy/modules/ext/*:$app/autopsy/modules/*:$app/platform/lib/*:$app/platform/modules/*"
mkdir -p build/qa-classes "$HOME/.cache/autopsy-qa/native"
javac -proc:none --release 21 -cp "$classpath" -d build/qa-classes tests/NativeSmoke.java
for fixture in ext4.raw ntfs.raw ext4.E01; do
    LD_LIBRARY_PATH="$app/native" "$app/runtime/bin/java" \
        -Dtsk.tmpdir="$HOME/.cache/autopsy-qa/native" \
        -Djava.library.path="$app/native" -cp "build/qa-classes:$classpath" \
        org.sleuthkit.datamodel.NativeSmoke "$PWD/build/fixtures with spaces/$fixture" \
        "$HOME/Casos de prueba á/$fixture"
done
