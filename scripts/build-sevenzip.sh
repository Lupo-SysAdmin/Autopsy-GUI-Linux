#!/bin/bash
# Build the matching Sleuth Kit fork; JDK 8 is a build tool, not the runtime.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/fetch.py sevenzip_source sevenzip_build_jdk
mkdir -p build/compliance/sevenzipjbinding-f308cd8f663cc3c013bfb14ec9cfc3ecc75c23f3 build/sevenzip-jdk
if [[ ! -f build/compliance/sevenzipjbinding-f308cd8f663cc3c013bfb14ec9cfc3ecc75c23f3/CMakeLists.txt ]]; then
    tar -xzf .cache/sevenzip-sleuthkit-f308cd8-source.tar.gz --strip-components=1 -C build/compliance/sevenzipjbinding-f308cd8f663cc3c013bfb14ec9cfc3ecc75c23f3
fi
if [[ ! -x build/sevenzip-jdk/bin/javac ]]; then
    tar -xzf .cache/OpenJDK8U-jdk_x64_linux_hotspot_8u512b09.tar.gz --strip-components=1 -C build/sevenzip-jdk
fi
cmake -S build/compliance/sevenzipjbinding-f308cd8f663cc3c013bfb14ec9cfc3ecc75c23f3 -B build/sevenzip-build \
    -DJAVA_JDK="$PWD/build/sevenzip-jdk" -DCMAKE_CXX_FLAGS=-std=gnu++98
cmake --build build/sevenzip-build -j"${BUILD_JOBS:-6}"
# Upstream tests share a native extraction cache: they must run serially.
(cd build/sevenzip-build && ctest --output-on-failure -j1)
python3 scripts/verify-sevenzip.py
