#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(dirname "$0")"

# Get the directory of the Python program (one level above the script)
PYTHON_DIR="$(realpath "$SCRIPT_DIR/..")"
PYTHON_PROGRAM="$PYTHON_DIR/pushback.py"

# Navigate to the desired directory
cd "$SCRIPT_DIR/../../JetsonWebDashboard/vexai-web-dashboard-react"

# Serve the build directory in the background
serve -s build
