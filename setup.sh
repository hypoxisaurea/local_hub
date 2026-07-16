#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$REPO_ROOT/.venv"
REQUIREMENTS_PATH="$REPO_ROOT/backend/requirements.txt"
PYTHON_VERSION_SCRIPT='import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'

create_venv() {
  local python_cmd="$1"

  if ! "$python_cmd" -c "$PYTHON_VERSION_SCRIPT"; then
    echo "Python 3.10+ is required. The '$python_cmd' command points to an older version." >&2
    exit 1
  fi

  "$python_cmd" -m venv "$VENV_PATH"
}

if [ ! -d "$VENV_PATH" ]; then
  if command -v python3 >/dev/null 2>&1; then
    create_venv python3
  elif command -v python >/dev/null 2>&1; then
    create_venv python
  else
    echo "Python 3 is required. Install Python 3.10+ and run this script again." >&2
    exit 1
  fi
fi

PYTHON_EXE="$VENV_PATH/bin/python"

if [ ! -x "$PYTHON_EXE" ]; then
  echo "Virtual environment was not created correctly: $PYTHON_EXE was not found." >&2
  exit 1
fi

"$PYTHON_EXE" -c "$PYTHON_VERSION_SCRIPT"
"$PYTHON_EXE" -m pip install --upgrade pip setuptools wheel
"$PYTHON_EXE" -m pip install -r "$REQUIREMENTS_PATH"

echo "Virtual environment ready at $VENV_PATH"
echo "Activate with: source .venv/bin/activate"
echo "Run backend and AI API with: npm run dev:backend"
echo "Run frontend with: npm run dev:frontend"
