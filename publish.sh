#!/usr/bin/env bash
# Publishes the scripts to Google Colab.
# Colab notebooks install the package straight from GitHub `main`, so publishing means:
# local checks -> git push -> check that GitHub serves an installable package.
set -euo pipefail

readonly GITHUB_REPO="nickolay-kondratyev/ximenas-tooling"
readonly PUBLISH_BRANCH="main"
readonly PACKAGE_NAME="ximenas_tooling"
# Same URL the notebooks' setup cell uses.
readonly PIP_INSTALL_URL="git+https://github.com/${GITHUB_REPO}.git@${PUBLISH_BRANCH}"
readonly COLAB_URL_PREFIX="https://colab.research.google.com/github/${GITHUB_REPO}/blob/${PUBLISH_BRANCH}"

REPO_ROOT="$(git rev-parse --show-toplevel)"
readonly REPO_ROOT
readonly VENV_DIR="${REPO_ROOT}/.tmp/publish-venv"
readonly LOG_FILE="${REPO_ROOT}/.tmp/publish.log"

fail() {
  echo "PUBLISH FAILED: $*" >&2
  exit 1
}

step() {
  echo "==> $*"
}

check_ready_to_publish() {
  step "Checking branch and working tree"
  local branch
  branch="$(git branch --show-current)"
  [[ "${branch}" == "${PUBLISH_BRANCH}" ]] \
    || fail "you are on branch=[${branch}]. Publishing only happens from ${PUBLISH_BRANCH}: git checkout ${PUBLISH_BRANCH}"
  [[ -z "$(git status --porcelain)" ]] \
    || fail "there are uncommitted changes. Commit or stash them first (see: git status)."
  [[ -f pyproject.toml ]] \
    || fail "no pyproject.toml at the repo root, so there is no package to publish yet."
}

run_local_checks() {
  step "Installing locally and running tests (log: ${LOG_FILE})"
  [[ -d "${VENV_DIR}" ]] || python3 -m venv "${VENV_DIR}"
  "${VENV_DIR}/bin/pip" install -q -e ".[dev]" >"${LOG_FILE}" 2>&1 \
    || fail "the package does not install locally. See log=[${LOG_FILE}]"
  "${VENV_DIR}/bin/python" -m pytest -q >>"${LOG_FILE}" 2>&1 \
    || fail "tests failed. See log=[${LOG_FILE}]"
}

push_to_github() {
  step "Pushing ${PUBLISH_BRANCH} to GitHub"
  git push origin "${PUBLISH_BRANCH}"
}

verify_installable_from_github() {
  step "Checking that Colab can install it from GitHub"
  # [--no-deps]: dependencies are already in the venv from the local checks; this only proves GitHub serves the package.
  "${VENV_DIR}/bin/pip" install -q --no-deps --force-reinstall "${PIP_INSTALL_URL}" >>"${LOG_FILE}" 2>&1 \
    || fail "pushed, but installing from GitHub failed. See log=[${LOG_FILE}]"
  # [-I]: isolated mode, so the import comes from the installed package, not ./src.
  "${VENV_DIR}/bin/python" -I -c "import ${PACKAGE_NAME}" >>"${LOG_FILE}" 2>&1 \
    || fail "pushed, but the package installed from GitHub does not import. See log=[${LOG_FILE}]"
}

print_colab_links() {
  step "Published. Colab links (send a link to the consumer only for NEW notebooks):"
  local notebook
  shopt -s nullglob
  for notebook in notebooks/*.ipynb; do
    echo "  ${COLAB_URL_PREFIX}/${notebook}"
  done
}

main() {
  cd "${REPO_ROOT}"
  mkdir -p "$(dirname "${LOG_FILE}")"
  check_ready_to_publish
  run_local_checks
  push_to_github
  verify_installable_from_github
  print_colab_links
}

main "$@"
