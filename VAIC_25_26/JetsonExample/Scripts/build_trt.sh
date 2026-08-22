#!/bin/bash
# Build TensorRT engine for the ONNX model. Run this on the Jetson Nano (TensorRT installed).
set -e
ONNX="models/pushback_lite.onnx"
TRT="models/pushback_lite.trt"
WORKSPACE_GB=2

echo "Checking for trtexec..."
if command -v trtexec >/dev/null 2>&1; then
  echo "Found trtexec — building engine via trtexec"
  trtexec --onnx="$ONNX" --saveEngine="$TRT" --explicitBatch --workspace=$(($WORKSPACE_GB * 1024))
  echo "Engine saved to $TRT"
else
  echo "trtexec not found — attempting Python builder using model_backend.py"
  python3 - <<'PY'
try:
    from model_backend import CUDABackend
    print('Using Python builder from model_backend')
    CUDABackend.get_engine('$ONNX', '$TRT')
    print('Engine built and saved to $TRT')
except Exception as e:
    print('Python builder failed:')
    import traceback
    traceback.print_exc()
    exit(1)
PY
fi

echo "Done."