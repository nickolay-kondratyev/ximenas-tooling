# Ximenas-tooling
Tooling for Ximena.
Ximena works as marketing data analyst.
She runs Python scripts in Google Colab.
Scripts that we create should work within Google Colab.

# Project CLI
- `ticket` for tracking items to be done and their order of doing them.
- `change_log` for tracking change log.

# Colab delivery conventions
- Repo is PUBLIC: never commit data files, client names/IDs, or secrets. Client-specific values come from notebook form inputs.
- Logic lives in the pip-installable package `src/ximenas_tooling/` with `pyproject.toml` at the repo root. Use loose dependency pins (e.g. `pandas>=2`) so Colab's preinstalled libs are reused. Provide a `dev` extra with `pytest` (`publish.sh` relies on it).
- Launcher notebooks live in `notebooks/`, stay thin, and have no committed outputs. Cells in order:
  1. Markdown: what it does and where it saves results.
  2. `%pip install -q git+https://github.com/nickolay-kondratyev/ximenas-tooling.git`
  3. Drive mount, if it touches files: `from google.colab import drive; drive.mount('/content/drive')`
  4. `# @param` form fields.
  5. One `run(...)` call.
- Publishing = `./publish.sh`. The human runs it, because it pushes `main`; agents do not. Manual steps: `docs/collab-setup/`.
