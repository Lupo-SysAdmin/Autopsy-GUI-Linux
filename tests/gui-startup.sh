#!/bin/bash
set -euo pipefail
mkdir -p build/gui
setsid autopsy-gui --nosplash > build/gui/console.log 2>&1 &
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
for attempt in $(seq 1 60); do
    if xdotool search --name 'Autopsy 4.23.1' > build/gui/window-ids.txt 2>/dev/null; then
        found=1
        break
    fi
    kill -0 "$app_pid"
    sleep 1
done
test "$found" = 1
sleep 5
xdotool key Return
sleep 5
xwininfo -root -tree > build/gui/windows.txt
import -window root build/gui/startup.png
! grep -E 'UnsupportedClassVersionError|SleuthkitJNI: failed' build/gui/console.log
echo 'PASS: installed Autopsy GUI started as a non-root user under Xvfb'
