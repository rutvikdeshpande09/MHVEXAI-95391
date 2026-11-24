#!/bin/bash

# Get the absolute directory of this script, regardless of the caller's cwd.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# Get the directory of the Python program (one level above the script)
PYTHON_DIR="$(realpath "$SCRIPT_DIR/..")"
PYTHON_PROGRAM="$PYTHON_DIR/pushback.py"

# Set the required environment variables
export PATH=$HOME/.pyenv/shims:/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6

# Run the Python program
exec python3 "$PYTHON_PROGRAM"
