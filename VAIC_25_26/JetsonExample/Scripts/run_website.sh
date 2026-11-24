#!/bin/bash

# Get the absolute directory of this script, regardless of the caller's cwd.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

DASHBOARD_DIR="$SCRIPT_DIR/../../JetsonWebDashboard/vexai-web-dashboard-react"
if [ ! -d "$DASHBOARD_DIR" ]; then
    echo "Web dashboard directory not found: $DASHBOARD_DIR" >&2
    echo "Copy JetsonWebDashboard/vexai-web-dashboard-react and run npm install && npm run build." >&2
    exit 1
fi

cd "$DASHBOARD_DIR" || exit 1

if [ ! -d build ]; then
    echo "Web dashboard build directory not found: $DASHBOARD_DIR/build" >&2
    echo "Build the dashboard first with: npm install && npm run build" >&2
    exit 1
fi

if command -v serve >/dev/null 2>&1; then
    exec serve -s build
fi

echo "The 'serve' command is unavailable; using Python HTTP server on port 3000."
exec python3 -m http.server 3000 --directory build
