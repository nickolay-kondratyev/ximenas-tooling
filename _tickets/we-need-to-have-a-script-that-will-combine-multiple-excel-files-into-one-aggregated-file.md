---
id: nid_6flt013tgdt5999nrwpyt76hr_e
title: "We need to have a script that will combine multiple excel files into one aggregated file"
status: open
deps: []
links: []
created_iso: 2026-09-18T04:19:47Z
status_updated_iso: 2026-09-18T04:19:47Z
type: task
priority: 3
assignee: nickolaykondratyev
tags: []
---

This script needs to be able to be run in google collab.

It needs to work on Excel files as input.

Input:
- multiple excel files
- each files has multiple tabs
  - we care about a single tab that we want to extract and combine with.
    - the tab name should be passed as an argument.
    - the columns names in this tab are expected to match (we can space normalize and lowercase prior to checking that they match, we are going to merge the data based on normalized column names).

OUTPUT:
- single excel file with all the rows from across the tabs.
- one extra column is added which contains the name of the source file that data came from.


