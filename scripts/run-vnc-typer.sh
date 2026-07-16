#!/bin/sh
set -eu
cd "$(dirname "$0")"

PYTHON_BIN="${VNC_TYPER_PYTHON:-}"
if [ -z "$PYTHON_BIN" ]; then
  for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      PYTHON_BIN="$(command -v "$candidate")"
      break
    fi
  done
fi

if [ -z "$PYTHON_BIN" ]; then
  echo "No Python 3 executable was found. Install Python 3 or set VNC_TYPER_PYTHON." >&2
  exit 1
fi

if [ ! -d .venv ]; then
  "$PYTHON_BIN" -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
