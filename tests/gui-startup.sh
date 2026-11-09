#!/bin/bash
# Check the real launcher without the Swing instrumentation agent.
set -euo pipefail
export LANG=C.UTF-8 LC_ALL=C.UTF-8
out="$PWD/build/gui-startup"
test ! -e "$out"
mkdir -p "$out"
export XDG_DATA_HOME="$out/data" XDG_CACHE_HOME="$out/cache"
setsid autopsy-gui > "$out/console.log" 2>&1 &
app_pid=$!
cleanup() {
    kill -TERM -- "-$app_pid" 2>/dev/null || true
    for attempt in $(seq 1 5); do
        kill -0 "$app_pid" 2>/dev/null || break
        sleep 1
    done
    kill -KILL -- "-$app_pid" 2>/dev/null || true
    wait "$app_pid" 2>/dev/null || true
}
trap cleanup EXIT
found=0
for attempt in $(seq 1 180); do
    # First-use Central Repository information can hide the main frame.
    if xdotool search --onlyvisible --name '^Information$' >/dev/null 2>&1; then
        xdotool key Return
    fi
    if xdotool search --onlyvisible --name 'Autopsy 4.23.1' > "$out/window-ids.txt" 2>/dev/null; then
        found=1
        break
    fi
    kill -0 "$app_pid"
    sleep 1
done
test "$found" = 1
sleep 5
xdotool key Return
sleep 15
kill -0 "$app_pid"
xwininfo -root -tree > "$out/windows.txt"
import -window root "$out/startup.png"
log="$XDG_DATA_HOME/autopsy-gui/var/log/messages.log"
test -s "$log"
cp "$log" "$out/platform.log"
! grep -E '^SEVERE|NoClassDefFoundError|ClassNotFoundException.*jdk.swing.interop' "$log"
! grep -E 'UnsupportedClassVersionError|SleuthkitJNI: failed' "$out/console.log"
printf '%s\n' 'PASS: uninstrumented launcher, visible GUI, and platform startup log' | tee "$out/PASS"
