#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
test "$(dpkg --print-architecture)" = amd64
python3 scripts/fetch.py
bash scripts/build-native.sh
python3 scripts/package.py
bash scripts/test-native.sh
python3 scripts/check-package.py
