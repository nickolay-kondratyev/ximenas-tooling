# Colab Setup — Running the Scripts

There's nothing to install or set up. You only need the notebook links from the script author.

## Every run
1. **Open the notebook link** (bookmark it). It always opens the latest version. Sign in to Google if asked.
2. **Read the text at the top.** It says what the script does and where it saves results.
3. **Fill in the form fields** (e.g. the input folder, the tab name). Folder paths start with `/content/drive/MyDrive/`, which is your "My Drive".
4. **Runtime → Run all.**
5. **Approve the prompts:**
   - **"Warning: This notebook was not authored by Google"**: click **Run anyway**.
   - **"Permit this notebook to access your Google Drive files?"**: click **Connect to Google Drive**, pick your account, and allow access. The script needs this to read your files and save results.
6. **Wait for it to finish.** The first cell installs the script, which can take up to a minute. The script then prints progress under the last cell, ending with a summary (e.g. where it saved the result).
7. **Open the result** in Google Drive at the location the summary shows.

To run again with different inputs, change the form fields and run all again.

Use the link each time instead of saving a copy to Drive. A saved copy won't get updates.

## If something goes wrong
1. Scroll to the error under the cell that failed and read it. Script errors explain what's wrong and how to fix it (e.g. a setting to change in the form).
2. Still stuck? Send the script author a screenshot of the error.
