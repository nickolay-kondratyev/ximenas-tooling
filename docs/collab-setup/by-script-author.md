# Colab Setup — Script Author (GitHub side)

Do these steps **before** handing scripts to the consumer. Then send them [by-consumer-in-collab.md](by-consumer-in-collab.md).

The repo is **private**, so Colab needs a read-only token to install our code.

## 1. Make the repo pip-installable
Logic lives in a Python package (`src/ximenas_tooling/`) with a `pyproject.toml` at the repo root.
Check that it installs:
```bash
pip install git+ssh://git@github.com/nickolay-kondratyev/ximenas-tooling.git
```

## 2. Create a read-only token (one-time)
GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**:

| Field | Value |
|---|---|
| Name | `ximenas-colab-read` |
| Expiration | 1 year (set a calendar reminder to rotate) |
| Repository access | **Only select repositories** → `ximenas-tooling` |
| Permissions | Repository → **Contents: Read-only** (nothing else) |

Send the token over a secure channel (e.g. a password-manager share), **not** plain email or chat.

## 3. Start each launcher notebook with this setup cell
```python
# Installs the latest ximenas-tooling from the private repo.
# Token comes from Colab Secrets so it never appears in the notebook.
from google.colab import userdata
_token = userdata.get('GITHUB_TOKEN')
%pip install -q "git+https://{_token}@github.com/nickolay-kondratyev/ximenas-tooling.git"
```
Each new Colab session starts clean, so this always installs the latest `main`.
Keep dependency pins loose (e.g. `pandas>=2`) so pip reuses Colab's preinstalled libraries.

Keep notebooks thin: setup cell → parameters (`# @param` form fields) → one `run(...)` call.

## 4. Share the launcher notebooks
Upload the `.ipynb` files from `notebooks/` to a Google Drive folder and share it with the consumer.

- **Logic changes** reach the consumer automatically on their next run.
- **Launcher changes** (new parameters) require re-sharing the notebook.

## Rotating / revoking the token
Generate a new token (step 2) and send it over. The consumer replaces the old value in Colab Secrets.
Revoke the old token on GitHub.
