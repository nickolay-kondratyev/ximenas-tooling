# Colab Setup — Running the Scripts

## One-time setup: save your access key
You'll get an access key (a long text starting with `github_pat_`) from the script author.

1. Open [Google Colab](https://colab.research.google.com) and open any notebook.
2. Click the **🔑 key icon** in the left sidebar.
3. Click **Add new secret**.
4. **Name:** `GITHUB_TOKEN` (exactly like this). **Value:** paste the key.

Colab saves this key in your Google account, so you only do this once.

## One-time per notebook: save your own copy
1. Open the shared Google Drive folder from the script author.
2. Right-click the notebook → **Open with → Google Colaboratory**.
3. **File → Save a copy in Drive**. From now on, use your copy.

## Every run
1. Open your copy of the notebook.
2. Fill in the form fields (e.g. the input folder).
3. **Runtime → Run all**.
4. Approve the prompts when asked:
   - **"Grant access to secret GITHUB_TOKEN"**: allow it.
   - **"Connect to Google Drive"**: allow it (needed to read your files and save results).

You always get the latest version of the scripts; there's nothing to update.

## If something goes wrong

| You see | Fix |
|---|---|
| `SecretNotFoundError` | The secret name must be exactly `GITHUB_TOKEN`. Check the 🔑 panel. |
| `Authentication failed` / `403` / `404` during install | The key expired or is wrong. Ask the script author for a new one, then replace the value in the 🔑 panel. |
| Anything else | Send the script author a screenshot of the error. |
