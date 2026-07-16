#!/bin/sh
set -eu
cd "$(dirname "$0")"

PYTHON_BIN="${VNC_TYPER_PYTHON:-}"
if [ -n "$PYTHON_BIN" ]; then
  if ! "$PYTHON_BIN" -c "import tkinter" >/dev/null 2>&1; then
    echo "VNC_TYPER_PYTHON does not have Tkinter support: $PYTHON_BIN" >&2
    exit 1
  fi
else
  for candidate in python3.13 python3.12 python3.11 python3.10 python3 /usr/bin/python3; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import tkinter" >/dev/null 2>&1; then
      PYTHON_BIN="$(command -v "$candidate")"
      break
    fi
  done
fi

if [ -z "$PYTHON_BIN" ]; then
  cat >&2 <<'MSG'
No Python with Tkinter support was found.

Install Python from https://www.python.org/downloads/macos/ or set VNC_TYPER_PYTHON to a Python executable that can run:
  python3 -c "import tkinter"
MSG
  exit 1
fi

if [ ! -d .venv ]; then
  "$PYTHON_BIN" -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
