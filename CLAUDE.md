# Ximenas-tooling
Tooling for Ximena.
Ximena works as marketing data analyst.
She runs Python scripts in Google Colab.
Scripts that we create should work within Google Colab.

# Project CLI
- `ticket` for tracking items to be done and their order of doing them.
- `change_log` for tracking change log.

# Layout
- Logic: `src/ximenas_tooling/` — pip-installable package, `pyproject.toml` at the repo root. Use loose dependency pins (e.g. `pandas>=2`) so Colab's preinstalled libs are reused. A `dev` extra provides `pytest` (`publish.sh` relies on it).
- Colab launcher notebooks: `notebooks/` — thin, no committed outputs. Cells in order:
  1. Markdown: what it does and where it saves results.
  2. `%pip install -q git+https://github.com/nickolay-kondratyev/ximenas-tooling.git`
  3. Drive mount, if it touches files: `from google.colab import drive; drive.mount('/content/drive')`
  4. `# @param` form fields.
  5. One `run(...)` call.

# Colab delivery conventions
- Repo is PUBLIC: never commit data files, client names/IDs, or secrets. Test `.xlsx` fixtures are generated in pytest `tmp_path`, never committed. Client-specific values come from notebook form inputs.
- Publishing = `./publish.sh`. The human runs it, because it pushes `main`; agents do not. Manual steps: `docs/collab-setup/how-to-use-in-google-colab.md`.

# Tests
- `./self_work.test.fast.sh`: pytest in `.tmp/venv` (editable install).
- `./self_work.test.full.sh`: clean non-editable `pip install .` + pytest.
