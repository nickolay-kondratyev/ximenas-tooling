# Colab Setup — Script Author (publishing)

What you do so the consumer can run scripts from a link. What they do is in [by-consumer-in-collab.md](by-consumer-in-collab.md).

The repo is **public**: no tokens or secrets are needed.

## 1. Never commit sensitive content
Anyone can read this repo. Keep out:
- Data files (client names, spend figures). `.gitignore` already blocks `*.xlsx`, `*.xls`, `*.csv`.
- Client-specific names or IDs in code. Take them as notebook form inputs instead.
- Secrets of any kind.

## 2. Put logic in the pip-installable package
Logic lives in `src/ximenas_tooling/` with a `pyproject.toml` at the repo root.
Keep dependency pins loose (e.g. `pandas>=2`) so pip reuses Colab's preinstalled libraries.

## 3. Write a thin launcher notebook in `notebooks/`
Cells, in order:
1. Markdown: what the script does, and where it saves results.
2. Setup: `%pip install -q git+https://github.com/nickolay-kondratyev/ximenas-tooling.git` (installs the latest `main` in every new Colab session).
3. Drive mount (if it reads/writes files): `from google.colab import drive; drive.mount('/content/drive')`
4. Form: parameters as `# @param` fields.
5. Run: one `run(...)` call.

## 4. Publish = `git push` to `main`
There is no separate publish step. The notebook and the logic update together, and consumers get the change on their next run.

## 5. Share the "Open in Colab" link (once per notebook)
```
https://colab.research.google.com/github/nickolay-kondratyev/ximenas-tooling/blob/main/notebooks/<notebook>.ipynb
```
Send it together with [by-consumer-in-collab.md](by-consumer-in-collab.md). The link always opens the latest `main`, so you don't need to re-share after pushing.
