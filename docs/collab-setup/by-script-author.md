# Colab Setup — Script Author (manual steps)

Manual steps to make scripts reachable from Google Colab. Coding conventions for the scripts themselves live in [CLAUDE.md](../../CLAUDE.md). What the consumer does is in [by-consumer-in-collab.md](by-consumer-in-collab.md).

## 1. Review before publishing
The repo is **public**. Check that the commits contain no client data, client names or secrets.

## 2. Publish
```bash
./publish.sh
```
It runs the tests, pushes `main` to GitHub, checks that the package installs from GitHub, and prints each notebook's Colab link.
The consumer gets the changes on their next run. Existing links keep working, so you don't need to re-share them.

## 3. New notebook only: share its link
Send the consumer the Colab link that `publish.sh` printed, together with [by-consumer-in-collab.md](by-consumer-in-collab.md).
