#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$REPO_ROOT/.venv"
REQUIREMENTS_PATH="$REPO_ROOT/requirements.txt"

if [ ! -d "$VENV_PATH" ]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 -m venv "$VENV_PATH"
  elif command -v python >/dev/null 2>&1; then
    python -m venv "$VENV_PATH"
  else
    echo "Python 3 is required. Install Python 3.11+ and run this script again." >&2
    exit 1
  fi
fi

PYTHON_EXE="$VENV_PATH/bin/python"

if [ ! -x "$PYTHON_EXE" ]; then
  echo "Virtual environment was not created correctly: $PYTHON_EXE was not found." >&2
  exit 1
fi

"$PYTHON_EXE" -m pip install --upgrade pip setuptools wheel
"$PYTHON_EXE" -m pip install -r "$REQUIREMENTS_PATH"

echo "Virtual environment ready at $VENV_PATH"
echo "Activate with: source .venv/bin/activate"
