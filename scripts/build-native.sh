#!/bin/bash
# Build only native TSK/JNI; use the matching Java JAR from the official ZIP.
set -euo pipefail
cd "$(dirname "$0")/.."
root=$PWD
export JAVA_HOME=${JAVA_HOME:-/usr/lib/jvm/java-21-openjdk-amd64}
test -f "$JAVA_HOME/include/jni.h"
python3 scripts/fetch.py sleuthkit
mkdir -p build
python3 -c 'import shutil; shutil.rmtree("build/sleuthkit-4.15.0", ignore_errors=True); shutil.rmtree("build/native", ignore_errors=True)'
tar -xzf .cache/sleuthkit-4.15.0.tar.gz -C build
cd build/sleuthkit-4.15.0
# The release tarball omits this header present in the same upstream tag.
cp "$root/packaging/upstream/tsk_lvm.hpp" tsk/pool/tsk_lvm.hpp
./configure --prefix=/opt/autopsy-gui/native --enable-java --disable-static
make -C tsk -j"${JOBS:-2}"
make -C bindings/java/jni -j"${JOBS:-2}"
mkdir -p "$root/build/native"
cp -a tsk/.libs/libtsk.so* bindings/java/jni/.libs/libtsk_jni.so* "$root/build/native/"
# Keep native libraries private to this application, including transitive lookup.
for lib in "$root"/build/native/*.so.*; do
    if [[ ! -L "$lib" ]]; then patchelf --set-rpath '$ORIGIN' "$lib"; fi
done
