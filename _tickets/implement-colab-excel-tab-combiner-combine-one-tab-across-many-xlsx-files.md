---
id: nid_goesnf8l5ia4fpkv4udjqp32j_e
title: "Implement Colab Excel tab combiner (combine one tab across many xlsx files)"
status: open
deps: []
links: []
created_iso: 2026-09-18T04:38:44Z
status_updated_iso: 2026-09-18T04:38:44Z
type: feature
priority: 2
assignee: nickolaykondratyev
tags: []
---

Implement a Google Colab tool for Ximena, a marketing data analyst. It combines ONE named tab from many Excel files into a single aggregated Excel file and adds a `Source File` column.

Planning ticket (closed): `_tickets/we-need-to-have-a-script-that-will-combine-multiple-excel-files-into-one-aggregated-file.md`.
Delivery conventions (READ FIRST): `docs/collab-setup/by-script-author.md` and `docs/collab-setup/by-consumer-in-collab.md`.

The repo is PUBLIC. Never commit data files or client names. `.gitignore` already blocks `*.xlsx`, `*.xls`, `*.csv`, so test fixtures MUST be generated at test time in pytest `tmp_path`.

## Files to create
- `pyproject.toml`: package `ximenas_tooling`, src layout, `requires-python = ">=3.10"`, deps `pandas>=2`, `openpyxl>=3` (loose pins so Colab's preinstalled libs are reused), optional dev extra `pytest`. It must install via `pip install git+https://github.com/nickolay-kondratyev/ximenas-tooling.git`.
- `src/ximenas_tooling/__init__.py`
- `src/ximenas_tooling/excel_combine/` package (suggested modules below)
- `notebooks/combine_excel_tabs.ipynb`: thin launcher notebook
- `tests/excel_combine/...`: pytest, BDD GIVEN/WHEN/THEN style, one assert per test where practical
- Update `CLAUDE.md` succinctly (how to run tests; where the package and notebooks live)

## Behavior (requirements)

### Inputs (parameters of `run(...)`)
- `input_folder: str`: Drive folder path, e.g. `/content/drive/MyDrive/reports`
- `tab_name: str`: the tab to extract from every file
- `output_file_name: str = "combined.xlsx"`
- `allow_column_mismatch: bool = False`: see "Column matching"

### File discovery
- Take every `*.xlsx` file DIRECTLY in `input_folder` (no subfolders), sorted by file name for deterministic output.
- Skip Excel lock files (`~$*.xlsx`) and the output file itself (same name as `output_file_name`), so reruns don't ingest the previous output.
- Ignore `.xls`/`.csv` (`.xls` would need `xlrd`; out of scope).
- No input files → error that names the folder.

### Normalization (ONE shared implementation, used for BOTH tab names and column names)
- `str(name)` → trim → collapse inner whitespace runs to a single space → lowercase.
- Example: `"  Campaign   Name "` → `"campaign name"`.

### Reading a tab
- Find the tab whose normalized name equals the normalized `tab_name`. If two tabs normalize to the same name → error.
- Header = row 1. Keep values as read (dates stay dates, numbers stay numbers). Formulas: use cached values (openpyxl default via pandas).
- Drop rows that are entirely empty (Excel often has trailing formatted-but-empty rows).
- Duplicate normalized column names within one tab → error.

### Validation: fail fast, but report ALL problems in ONE error
Collect every problem across all files, then raise a single `CombineValidationError` whose message is plain language and lists each problem per file. Nothing is written when validation fails.
- A file lacks the tab → list the file and the tab names it DOES have.
- Duplicate normalized columns within a tab.
- Column mismatch (below) when `allow_column_mismatch` is False.

### Column matching (HUMAN requirement: LOUD failure by default)
- SCOPE: only the extracted tab (`tab_name`) is compared. Other tabs in each workbook are never read or validated; their columns are irrelevant.
- The normalized column SET of the extracted tab must match exactly across ALL files; column ORDER may differ.
- By default (`allow_column_mismatch=False`), any mismatch FAILS THE ENTIRE RUN LOUDLY. The error must:
  - start with a clear banner, e.g. `COLUMN MISMATCH — nothing was written.`
  - list, per file, `missing: [...]` and `unexpected: [...]` columns relative to the first file (reference = first file in sorted order; name it in the message)
  - end by telling the user exactly how to override: `To combine anyway (missing values left blank), set allow_column_mismatch = True in the notebook form and run again.` The message MUST contain the literal parameter name `allow_column_mismatch`.
- With `allow_column_mismatch=True`: combine the UNION of columns (never drop data). Cells are blank where a file lacks a column. Print a loud WARNING block listing the same per-file mismatch details, then proceed.

### Output
- Column headers use the ORIGINAL header text from the first file that has that column. Order = first file's column order, then extra columns (union mode only) in order of first appearance across the sorted files.
- Append a final column `Source File` holding the file name (e.g. `Q1_report.xlsx`, not the full path). If any input already has a column that normalizes to `source file` → error.
- Write to `<input_folder>/<output_file_name>`, one sheet named after `tab_name` as given (truncate to Excel's 31-char sheet-name limit with a named constant), overwriting any existing file.
- Console feedback: row count per file, total rows, output path.

## Suggested design (small, SRP classes; no free-floating public functions)
- `ColumnNameNormalizer`: static `normalize(name) -> str`. The single source of the normalization rule.
- `SourceTable` (dataclass): `file_name: str`, `frame: pandas.DataFrame`. Avoid tuples/pairs.
- `ExcelTabReader`: reads one file's matching tab into a `SourceTable`, or records a problem.
- `ColumnMismatch` (dataclass): `file_name`, `missing: list[str]`, `unexpected: list[str]`.
- `TabCombiner`: pure pandas. Takes `list[SourceTable]` + `allow_column_mismatch`, validates, and returns the combined DataFrame (with `Source File`). Easiest to unit test without files.
- `CombineValidationError(Exception)`: holds a list of problem strings and formats the loud message.
- `ExcelCombineJob.run(input_folder, tab_name, output_file_name="combined.xlsx", allow_column_mismatch=False)`: discovery → read → combine → write → print summary. Expose `run` from `ximenas_tooling.excel_combine` for the notebook.
- Constants for `Source File`, `.xlsx`, the `~$` prefix, and the 31-char limit.

## Notebook `notebooks/combine_excel_tabs.ipynb`
Keep it thin, per `docs/collab-setup/by-script-author.md`:
1. Markdown cell: one-paragraph description plus "Runtime → Run all".
2. Setup cell: `%pip install -q git+https://github.com/nickolay-kondratyev/ximenas-tooling.git`
3. Drive mount: `from google.colab import drive; drive.mount('/content/drive')`
4. Form cell: `input_folder = "/content/drive/MyDrive/" # @param {type:"string"}`, `tab_name = "" # @param {type:"string"}`, `output_file_name = "combined.xlsx" # @param {type:"string"}`, `allow_column_mismatch = False # @param {type:"boolean"}`
5. Run cell: `from ximenas_tooling.excel_combine import run` then `run(input_folder, tab_name, output_file_name, allow_column_mismatch)`
The notebook must be valid JSON (nbformat 4) with no outputs committed.

## Tests (pytest, fixtures generated via pandas/openpyxl into tmp_path)
Cover at least:
- normalizer: trim, collapse whitespace, lowercase, non-str input
- happy path: 2–3 files, matching columns in different order/case/spacing → all rows present, `Source File` correct, headers from the first file
- tab matched case/space-insensitively; missing tab → error lists file and its available tabs
- other tabs with differing columns across files do NOT cause a mismatch (only the extracted tab is compared)
- column mismatch default → raises; message contains `allow_column_mismatch`, `missing`, `unexpected`, file names; NO output file written
- column mismatch + `allow_column_mismatch=True` → union of columns, blanks where missing, row count correct
- multiple problems across files reported in ONE error
- duplicate normalized columns → error; existing `Source File` column → error
- fully empty rows dropped
- lock files and the previous output file are skipped; no input files → error
- end-to-end `run(...)` writes the output file with the expected sheet name

## Acceptance Criteria

- `pip install .` works in a clean venv; `pytest` passes (all tests listed above).
- Default run with mismatched normalized columns fails loudly, writes nothing, and the message names `allow_column_mismatch`.
- `allow_column_mismatch=True` produces the union of columns with blanks and prints a warning.
- `notebooks/combine_excel_tabs.ipynb` follows the thin launcher shape from `docs/collab-setup/by-script-author.md`.
- No `.xlsx`/data files committed. `CLAUDE.md` updated succinctly. `change_log` entry added.

