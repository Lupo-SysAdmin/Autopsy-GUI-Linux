#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build/fixture-files
printf 'Autopsy Linux fixture / Evidencia de prueba\n' > build/fixture-files/evidence.txt
truncate -s 32M build/native-fixture.img
mkfs.ext4 -q -F -d build/fixture-files build/native-fixture.img
