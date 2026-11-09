#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
app=${AUTOPSY_GUI_HOME:-"$PWD/build/package/opt/autopsy-gui"}
mkdir -p build/test-classes
bash scripts/make-fixture.sh
classpath="$app/autopsy/modules/ext/*:$app/autopsy/modules/*:$app/platform/lib/*:$app/platform/modules/*"
"${JAVA_HOME:-/usr/lib/jvm/java-21-openjdk-amd64}/bin/javac" \
    -proc:none --release 21 -cp "$classpath" -d build/test-classes tests/NativeSmoke.java
LD_LIBRARY_PATH="$app/native" "$app/runtime/bin/java" \
    -Djava.library.path="$app/native" -cp "build/test-classes:$classpath" \
    org.sleuthkit.datamodel.NativeSmoke "$PWD/build/native-fixture.img"
