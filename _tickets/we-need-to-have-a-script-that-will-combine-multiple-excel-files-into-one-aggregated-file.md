---
closed_iso: 2026-09-18T04:38:48Z
id: nid_6flt013tgdt5999nrwpyt76hr_e
title: We need to have a script that will combine multiple excel files into one aggregated
  file
status: closed
deps: []
links: []
created_iso: '2026-09-18T04:19:47Z'
status_updated_iso: 2026-09-18T04:38:48Z
type: task
priority: 3
assignee: nickolaykondratyev
tags: []
pwd: /home/nickolaykondratyev/git_repos/nickolay-kondratyev_ximenas-tooling
---
--------------------------------------------------------------------------------
TASK: **PLAN**. Reach a shared understanding of this ticket before writing any plan.

## Interview
Treat the work as a design tree: each decision unlocks the decisions below it. Work in rounds. Each round, ask every question whose prerequisites are settled; questions that depend on an open question wait for a later round.

Split decisions into two kinds:
- **AGENT decides**: anything a fact settles, or where one option is clearly right. Find facts yourself (dispatch `Explore-cheap` for code base or environment questions; don't block the round on it). Decide, and list each decision with a one-line reason so the HUMAN can veto.
- **HUMAN decides**: true judgment calls: tradeoffs, scope, product intent, anything the AGENT would only be guessing at. Put each to the HUMAN and wait.

A question goes to the HUMAN only if it clears this bar: the answer changes the plan, AND it cannot be settled by a fact, AND the ticket, code base, or conventions don't already imply the answer. If the answer could be inferred with reasonable confidence, make the call under AGENT decides and let the HUMAN veto. Do NOT ask questions to appear thorough. Zero questions is a valid and expected outcome for a clear ticket.

## Asking
Do NOT use AskUserQuestion. Each round, overwrite `.out/current_decision.md` (git-ignored) with:
1. A concise summary of the problem and the key tradeoffs.
2. **AGENT decided**: what you settled yourself, one line each.
3. **HUMAN decides**: the numbered questions, formatted:

❓ **Q1** - **<title>**: <question, may include options>

➡️ <AGENT's recommendation>

---

Then tell the HUMAN to read the file and reply. After each reply, recompute the frontier and ask the next round. Done when nothing is left to ask and the HUMAN confirms a shared understanding.

If the first round produces no HUMAN questions, still write the file (summary plus AGENT decided), tell the HUMAN it needs only a veto pass, and proceed to Output once they confirm or after they reply with no objections. Do not manufacture questions to fill the section.

## Output
Only after that confirmation, write the detailed plan with requirements.
IF multiple tickets are needed
THEN put the high-level plan into a new ticket and `close` it,
AND create focused implementation tickets with `ticket dep <impl-id> <plan-id>`
ELSE put the plan into a new `open` ticket.
Split so each ticket fits in a 200K context window and is self contained: full relative paths from git root, key details included, since a less capable model will execute it.
Finally `close` this ticket.
IF any ticket needs a higher tier model to implement it, then set higher profile with CLI `ticket profile <id> higher`.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
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

## Notes

**2026-09-18T04:38:47Z**

Planning done. HUMAN confirmed decisions and added a requirement: normalized column mismatch across ANY file fails the entire run loudly unless allow_column_mismatch=True (then union of columns, blanks, warning). Implementation: nid_goesnf8l5ia4fpkv4udjqp32j_e
