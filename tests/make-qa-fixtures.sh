#!/bin/bash
set -euo pipefail
bash scripts/make-fixture.sh
mkdir -p 'build/fixtures with spaces'
cp build/native-fixture.img 'build/fixtures with spaces/ext4.raw'
truncate -s 64M 'build/fixtures with spaces/ntfs.raw'
mkntfs -F -Q 'build/fixtures with spaces/ntfs.raw'
ntfscp -f 'build/fixtures with spaces/ntfs.raw' build/fixture-files/evidence.txt /evidence.txt
ewfacquire -u -f encase6 -c fast -t 'build/fixtures with spaces/ext4' 'build/fixtures with spaces/ext4.raw'
sha256sum 'build/fixtures with spaces/'* > build/fixture-SHA256SUMS
