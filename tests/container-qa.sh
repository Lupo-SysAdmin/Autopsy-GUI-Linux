#!/bin/bash
# Destructive package lifecycle tests ONLY inside a disposable container.
set -euo pipefail
test -f /.dockerenv
export DEBIAN_FRONTEND=noninteractive
export LANG=C.UTF-8 LC_ALL=C.UTF-8
mkdir -p /work
tar -C /src --exclude='./.git' --exclude='./.cache' --exclude='./build' --exclude='./dist' -cf - . | tar -C /work -xf -
cd /work
mkdir -p build
exec > >(tee /results/lifecycle.log) 2>&1
cat /etc/os-release
sha256sum /artifacts/autopsy-gui_4.23.1-4_amd64.deb
apt-get update
apt-get install -y --no-install-recommends default-jdk-headless desktop-file-utils \
    e2fsprogs ntfs-3g ewf-tools p7zip-full xvfb xauth xdotool x11-utils imagemagick python3 \
    autopsy /artifacts/autopsy-gui_4.23.1-4_amd64.deb
test "$(dpkg-query -W -f='${Status}' autopsy-gui)" = 'install ok installed'
sha256sum /usr/bin/autopsy > build/legacy-SHA256SUMS
autopsy-gui --diagnose
desktop-file-validate /usr/share/applications/autopsy-gui.desktop
id autopsyqa >/dev/null 2>&1 || useradd -m -s /bin/bash autopsyqa
chown -R autopsyqa:autopsyqa /work
runuser -u autopsyqa -- bash tests/make-qa-fixtures.sh
runuser -u autopsyqa -- bash tests/archive-qa.sh
runuser -u autopsyqa -- bash tests/installed-data-qa.sh
runuser -u autopsyqa -- xvfb-run -a -s '-screen 0 1440x1000x24' bash tests/gui-startup.sh
runuser -u autopsyqa -- xvfb-run -a -s '-screen 0 1440x1000x24' python3 tests/gui-regression.py
find '/home/autopsyqa/Casos de prueba á' -type f -exec sha256sum '{}' + > build/cases-before.sha256
# A synthetic higher package revision exercises dpkg's upgrade path.
dpkg-deb -R /artifacts/autopsy-gui_4.23.1-4_amd64.deb /tmp/upgrade-package
sed -i 's/^Version: .*/Version: 4.23.1-4+qa1/' /tmp/upgrade-package/DEBIAN/control
dpkg-deb -Zgzip -z1 --root-owner-group --build /tmp/upgrade-package /tmp/upgrade.deb
apt-get install -y /tmp/upgrade.deb
sha256sum -c build/cases-before.sha256
runuser -u autopsyqa -- bash tests/installed-data-qa.sh
apt-get remove -y autopsy-gui
test ! -e /usr/bin/autopsy-gui
sha256sum -c build/cases-before.sha256
sha256sum -c build/legacy-SHA256SUMS
apt-get install -y --no-install-recommends /artifacts/autopsy-gui_4.23.1-4_amd64.deb
apt-get purge -y autopsy-gui
test ! -e /opt/autopsy-gui
sha256sum -c build/cases-before.sha256
apt-get install -y --no-install-recommends /artifacts/autopsy-gui_4.23.1-4_amd64.deb
runuser -u autopsyqa -- bash tests/installed-data-qa.sh
dpkg-query -W -f='${binary:Package}\t${Version}\t${Status}\n' > /results/packages.tsv
cp -a build/gui-regression build/gui-startup /results/
cp build/*SHA256SUMS build/cases-before.sha256 /results/
echo 'PASS: clean install, coexistence, native data tests, GUI case/ingest/search/report, synthetic upgrade, remove, purge, reinstall'
touch /results/PASS
