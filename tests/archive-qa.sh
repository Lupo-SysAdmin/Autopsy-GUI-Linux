#!/bin/bash
set -euo pipefail
app=${AUTOPSY_GUI_HOME:-/opt/autopsy-gui}
mkdir -p 'build/archive fixtures' build/archive-classes
printf 'Autopsy archive fixture á\n' > 'build/archive fixtures/evidencia á.txt'
# Unique output directories are required, so an old archive cannot mask a regression.
for name in sample.zip encrypted.zip encrypted.7z; do
    test ! -e "build/archive fixtures/$name"
done
(cd 'build/archive fixtures' && 7z a -tzip sample.zip 'evidencia á.txt' >/dev/null &&
  7z a -tzip -ptest-password encrypted.zip 'evidencia á.txt' >/dev/null &&
  7z a -t7z -ptest-password encrypted.7z 'evidencia á.txt' >/dev/null)
cp="$app/autopsy/modules/ext/sevenzipjbinding.jar:$app/autopsy/modules/ext/sevenzipjbinding-AllPlatforms.jar"
javac -proc:none --release 21 -cp "$cp" -d build/archive-classes tests/ArchiveSmoke.java
"$app/runtime/bin/java" -cp "build/archive-classes:$cp" ArchiveSmoke \
    'build/archive fixtures/sample.zip' 'build/archive fixtures/encrypted.zip' 'build/archive fixtures/encrypted.7z'
