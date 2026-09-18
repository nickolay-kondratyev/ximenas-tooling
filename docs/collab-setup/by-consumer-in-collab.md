# Colab Setup — Running the Scripts

You don't install anything. The notebook installs the script by itself each time it runs.

## One-time setup
1. **Sign in to Google in your browser with the account that holds your files** (your Google Drive account).
2. **Bookmark each notebook link** the script author sent you. Always open the notebook from the bookmark. A copy saved to Drive won't get updates.
3. **Put your input files in a folder in "My Drive"**, e.g. `My Drive/reports`. Upload them at drive.google.com (**New → Folder upload**).
   - Folder shared with you by someone else? It isn't in "My Drive" by default. In Drive, right-click it → **Organize → Add shortcut** → pick **My Drive**.
4. **Learn how folder paths look.** The form asks for paths like `/content/drive/MyDrive/reports`. `/content/drive/MyDrive/` means your "My Drive", followed by the folder name exactly as shown in Drive.
   - To copy the exact path: after the notebook has run once, click the **folder icon** in Colab's left sidebar → `drive` → `MyDrive` → right-click your folder → **Copy path**.

## Every run
1. **Open the notebook bookmark.** Sign in to Google if asked.
2. **Read the text at the top.** It says what the script does and where it saves results.
3. **Fill in the form fields** (e.g. the input folder, the tab name).
4. **Runtime → Run all.**
5. **Approve the prompts:**
   - **"Warning: This notebook was not authored by Google"**: click **Run anyway**.
   - **"Permit this notebook to access your Google Drive files?"**: click **Connect to Google Drive**, pick the account from setup step 1, and allow access. The script needs this to read your files and save results.
6. **Wait for it to finish.** The first cell installs the script, which can take up to a minute. The script then prints progress under the last cell, ending with a summary (e.g. where it saved the result).
7. **Open the result** in Google Drive at the location the summary shows.

To run again with different inputs, change the form fields and run all again.

## If something goes wrong
1. Scroll to the error under the cell that failed and read it. Script errors explain what's wrong and how to fix it (e.g. a setting to change in the form).
2. `No such file or directory` for a folder? Check the path against setup step 4.
3. Still stuck? Send the script author a screenshot of the error.
