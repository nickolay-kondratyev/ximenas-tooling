# Colab Setup — Script Author (GitHub side)

Do these steps **before** handing scripts to the consumer. Then send them [by-consumer-in-collab.md](by-consumer-in-collab.md).

The repo is **public**: no tokens or secrets are needed.

## 1. Never commit sensitive content
Anyone can read this repo. Keep out:
- Data files (client names, spend figures). `.gitignore` already blocks `*.xlsx`, `*.xls`, `*.csv`.
- Client-specific names or IDs in code. Take them as notebook form inputs instead.
- Secrets of any kind.

## 2. Make the repo pip-installable
Logic lives in a Python package (`src/ximenas_tooling/`) with a `pyproject.toml` at the repo root.
Keep dependency pins loose (e.g. `pandas>=2`) so pip reuses Colab's preinstalled libraries.
Publishing is just `git push` to `main`. There is no separate publish step.

After pushing, check that it installs. This command only downloads from GitHub, so it tests what is pushed, not your local changes:
```bash
pip install git+https://github.com/nickolay-kondratyev/ximenas-tooling.git
```

## 3. Start each launcher notebook with this setup cell
```python
%pip install -q git+https://github.com/nickolay-kondratyev/ximenas-tooling.git
```
Each new Colab session starts clean, so this always installs the latest `main`.

Keep notebooks thin: setup cell → parameters (`# @param` form fields) → one `run(...)` call.

## 4. Share the "Open in Colab" link
For each notebook in `notebooks/`, send the consumer:
```
https://colab.research.google.com/github/nickolay-kondratyev/ximenas-tooling/blob/main/notebooks/<notebook>.ipynb
```
The link always opens the latest version from `main`. Pushing to `main` updates both the notebook and the logic, with no re-sharing.
