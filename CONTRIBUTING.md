# Contributing observations

The dataset grows one real scan at a time.

## How to contribute

1. Install [header-hunter](https://github.com/Iceman2050/header-hunter) (zero dependencies, Python 3.10+).
2. Scan a site:
   ```sh
   python3 headerhunter.py https://example.com --json > my-scan.json
   ```
3. Open a PR adding your scan output (the raw `results` array) — a maintainer converts it into the v0.1 schema, or convert it yourself following `SCHEMA.md`.

## Rules

- **Only real tool outputs.** Do not hand-write observations, do not edit header values, do not invent scans.
- One scan per site per dataset file; re-scans go into the newest dated file.
- Be respectful: the scanner already rate-limits (one request per URL, timeouts, redirect caps). Do not hammer sites.
- Do not submit scans of sites you don't have a legitimate reason to fetch headers from (public homepages, docs, and APIs are fine).
- `suspicious` findings are *possible* injection attempts, never confirmed attacks — keep the wording honest in any write-up.

## What happens next

Accepted observations land in the next dated dataset file, the stats regenerate via `tools/stats.py`, and the site updates. Contributors are credited in the dataset file's commit message.
