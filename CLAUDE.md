# Ximenas-tooling
Tooling for Ximena.
Ximena works as marketing data analyst.
She runs Python scripts in Google Colab.
Scripts that we create should work within Google Colab.

# Project CLI
- `ticket` for tracking items to be done and their order of doing them.
- `change_log` for tracking change log.
# Layout
- Logic: `src/ximenas_tooling/` (pip-installable; Colab installs it from GitHub `main`).
- Colab launcher notebooks: `notebooks/` (thin: install → form → `run(...)`). See `docs/collab-setup/`.
- Public repo: test `.xlsx` fixtures are generated in pytest `tmp_path`, never committed.

# Tests
- `./self_work.test.fast.sh`: pytest in `.tmp/venv` (editable install).
- `./self_work.test.full.sh`: clean non-editable `pip install .` + pytest.
