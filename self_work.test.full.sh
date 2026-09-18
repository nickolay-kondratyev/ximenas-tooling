#!/usr/bin/env bash
# Verifies a clean, non-editable `pip install .` (as Colab does) and runs the tests against it.
set -euo pipefail
cd "$(dirname "$0")"

VENV=.tmp/venv-full
rm -rf "${VENV}"
python3 -m venv "${VENV}"
"${VENV}/bin/pip" install -q ".[dev]"
# src/ layout: `ximenas_tooling` is importable only from the installed package, never from the checkout.
"${VENV}/bin/pytest" -q -p no:cacheprovider "$@"
