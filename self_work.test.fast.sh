#!/usr/bin/env bash
# Runs the test suite in the repo-local venv (created on first run).
set -euo pipefail
cd "$(dirname "$0")"

VENV=.tmp/venv
if [[ ! -x "${VENV}/bin/pytest" ]]; then
  python3 -m venv "${VENV}"
  "${VENV}/bin/pip" install -q -e ".[dev]"
fi
"${VENV}/bin/pytest" -q "$@"
