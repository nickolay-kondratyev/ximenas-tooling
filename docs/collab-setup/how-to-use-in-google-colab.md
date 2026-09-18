# How to Use in Google Colab

- **Part 1** is for the person running the scripts.
- **Part 2** is for the script author who publishes them.

## Part 1: Running the scripts
You don't install anything. The notebook installs the script by itself each time it runs.

The steps below use the **combine_excel_tabs** notebook as the example: it takes one tab (e.g. `Sales`) from every Excel file in a Drive folder and stacks them into one Excel file in that same folder. Other notebooks work the same way; only the form fields differ.

### One-time setup
1. **Sign in to Google in your browser with the account that holds your files** (your Google Drive account).
2. **Bookmark each notebook link** the script author sent you (e.g. the combine_excel_tabs link). Always open the notebook from the bookmark. A copy saved to Drive won't get updates.
3. **Put your input files in a folder in "My Drive"**, e.g. `My Drive/reports` holding `january.xlsx`, `february.xlsx`, `march.xlsx`. Upload them at drive.google.com (**New → Folder upload**).
   - Folder shared with you by someone else? It isn't in "My Drive" by default. In Drive, right-click it → **Organize → Add shortcut** → pick **My Drive**.
4. **Learn how folder paths look.** The form asks for paths like `/content/drive/MyDrive/reports`. `/content/drive/MyDrive/` means your "My Drive", followed by the folder name exactly as shown in Drive.
   - To copy the exact path: after the notebook has run once, click the **folder icon** in Colab's left sidebar → `drive` → `MyDrive` → right-click your folder → **Copy path**.

### Every run
1. **Open the notebook bookmark.** Sign in to Google if asked.
2. **Read the text at the top.** It says what the script does and where it saves results.
3. **Fill in the form fields.** For combine_excel_tabs:

   | Field | Example | Meaning |
   |---|---|---|
   | `input_folder` | `/content/drive/MyDrive/reports` | Folder with the Excel files (see setup step 4). Subfolders are not read. |
   | `tab_name` | `Sales` | The tab to take from each file. Upper/lower case and extra spaces don't matter. |
   | `output_file_name` | `combined.xlsx` | Name of the result file, saved in `input_folder`. Running again overwrites it. |
   | `allow_column_mismatch` | unchecked | Leave unchecked. Check it only if the files' columns differ and you want to combine anyway (see below). |

4. **Runtime → Run all.**
5. **Approve the prompts:**
   - **"Warning: This notebook was not authored by Google"**: click **Run anyway**.
   - **"Permit this notebook to access your Google Drive files?"**: click **Connect to Google Drive**, pick the account from setup step 1, and allow access. The script needs this to read your files and save results.
6. **Wait for it to finish.** The first cell installs the script, which can take up to a minute. The script then prints progress under the last cell, ending with a summary, e.g.:
   ```
   Read rows=[120] from file=[february.xlsx]
   Read rows=[98] from file=[january.xlsx]
   Read rows=[134] from file=[march.xlsx]
   Total rows=[352] from files=[3]
   Wrote output=[/content/drive/MyDrive/reports/combined.xlsx]
   ```
7. **Open the result** in Google Drive at the location the summary shows (here: `My Drive/reports/combined.xlsx`). Its `Source File` column shows which file each row came from.

To run again with different inputs (e.g. another tab), change the form fields and run all again.

### If something goes wrong
1. Scroll to the error under the cell that failed and read it. Script errors say that nothing was written, what's wrong, and how to fix it (e.g. a setting to change in the form). All problems are listed at once, so you can fix them in one go.
2. Common combine_excel_tabs errors:
   - `Folder not found`: check `input_folder` against setup step 4.
   - `tab [...] not found`: the error lists the tabs that file does have. Fix `tab_name`, or rename the tab in that file.
   - `COLUMN MISMATCH`: the files' columns differ; the error lists which file has which columns. Fix the files, or check `allow_column_mismatch` to combine anyway (cells are left blank where a file lacks a column).
3. Still stuck? Send the script author a screenshot of the error.

## Part 2: Script author (publishing)
Manual steps to make scripts reachable from Google Colab. Coding conventions for the scripts themselves live in [CLAUDE.md](../../CLAUDE.md).

### 1. Review before publishing
The repo is **public**. Check that the commits contain no client data, client names or secrets.

### 2. Publish
```bash
./publish.sh
```
It runs the tests, pushes `main` to GitHub, checks that the package installs from GitHub, and prints each notebook's Colab link.
The consumer gets the changes on their next run. Existing links keep working, so you don't need to re-share them.

### 3. New notebook only: share its link
Send the consumer the Colab link that `publish.sh` printed, together with this doc (Part 1 is for them).
