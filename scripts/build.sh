#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
test "$(dpkg --print-architecture)" = amd64
python3 scripts/fetch.py
python3 scripts/bundle-third-party.py --fetch-only
bash scripts/build-native.sh
bash scripts/build-sevenzip.sh
python3 scripts/package.py
bash scripts/test-native.sh
python3 scripts/check-package.py
