#!/bin/bash
# Run in a disposable test container after installing the package.
set -euo pipefail
app=/opt/autopsy-gui
autopsy-gui --diagnose
test -x "$app/runtime/bin/java"
desktop-file-validate /usr/share/applications/autopsy-gui.desktop
temp=$(mktemp -d)
trap 'rm -rf "$temp"' EXIT
classpath="$app/autopsy/modules/ext/*:$app/autopsy/modules/*:$app/platform/lib/*:$app/platform/modules/*"
bash scripts/make-fixture.sh
javac -proc:none --release 21 -cp "$classpath" -d "$temp" tests/NativeSmoke.java
LD_LIBRARY_PATH="$app/native" "$app/runtime/bin/java" \
    -Djava.library.path="$app/native" -cp "$temp:$classpath" org.sleuthkit.datamodel.NativeSmoke "$PWD/build/native-fixture.img"
