#!/bin/bash

# Get the absolute directory of this script, regardless of the caller's cwd.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# Get the directory of the Python program (one level above the script)
PYTHON_DIR="$(realpath "$SCRIPT_DIR/..")"
PYTHON_PROGRAM="$PYTHON_DIR/pushback.py"

DASHBOARD_DIR="$SCRIPT_DIR/../../JetsonWebDashboard/vexai-web-dashboard-react"
if [ ! -d "$DASHBOARD_DIR" ]; then
    echo "Web dashboard directory not found: $DASHBOARD_DIR" >&2
    echo "Copy JetsonWebDashboard/vexai-web-dashboard-react into the repository first." >&2
    exit 1
fi

cd "$DASHBOARD_DIR" || exit 1

# Serve the build directory in the background
if [ ! -d build ]; then
    echo "Web dashboard build directory not found: $DASHBOARD_DIR/build" >&2
    echo "Build it with: cd \"$DASHBOARD_DIR\" && npm install && npm run build" >&2
    exit 1
fi

if command -v serve >/dev/null 2>&1; then
    serve -s build &
else
    echo "The 'serve' command is unavailable; using Python HTTP server on port 3000."
    python3 -m http.server 3000 --directory build &
fi

# Set the required environment variables
export PATH=$HOME/.pyenv/shims:/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6

# Run the Python program
exec python3 "$PYTHON_PROGRAM"
