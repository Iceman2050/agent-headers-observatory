#!/usr/bin/env python3
"""Render site/index.html from the dataset. All numbers come from
tools/stats.py — nothing is hand-typed. Token replacement is used
instead of %-formatting so CSS percent signs can't break the build.

Usage: python3 tools/build_site.py   (run from the repo root)
"""
from __future__ import annotations

import html
import json
from pathlib import Path

from stats import compute

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent Headers Observatory — which sites talk to AI agents via HTTP headers</title>
<meta name="description" content="A public, versioned dataset of websites that communicate with AI agents through HTTP headers. Seeded with real scans; community-built.">
<style>
body{font-family:system-ui,-apple-system,sans-serif;max-width:860px;margin:2rem auto;padding:0 1rem;color:#1a1a1a;line-height:1.6}
.stat{display:inline-block;margin:0 1.5rem 1rem 0}.stat b{font-size:2rem;display:block}
table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ddd;padding:.5rem;text-align:left}
code{background:#f4f4f4;padding:.1rem .3rem;border-radius:3px;word-break:break-all}
.note{background:#fff8e1;border:1px solid #f0d060;padding:1rem;border-radius:6px}
footer{margin-top:2rem;color:#666;font-size:.9rem}
</style>
</head>
<body>
<h1>Agent Headers Observatory</h1>
<p>The public dataset of websites that talk to AI agents through HTTP headers.
Seeded October 2026, after researchers found ~8,000 sites using headers to
reach AI agents — and 30 attempting indirect prompt injection through them.</p>

<h2>Dataset v0.1 — at a glance</h2>
<div class="stat"><b>@@SITES@@</b>sites observed</div>
<div class="stat"><b>@@AD@@</b>agent-directed</div>
<div class="stat"><b>@@SUSP@@</b>suspicious</div>
<div class="stat"><b>@@ERR@@</b>failed scans</div>
<p><small>Dataset file: <code>@@DSFILE@@</code> · generated @@GEN@@ · schema v@@SCHEMA@@.
Numbers on this page are computed from the dataset by <code>tools/stats.py</code>.</small></p>

<h2>Sites with agent-directed or suspicious headers</h2>
<table>
<tr><th>Site</th><th>Verdict</th><th>Header</th><th>Value (truncated)</th></tr>
@@ROWS@@
</table>

<h2>Most common flagged header names</h2>
<table>
<tr><th>Header</th><th>Sites</th></tr>
@@TOP@@
</table>

<div class="note">
<strong>Methodology &amp; honest limits.</strong> Every observation is a real run of
<a href="https://github.com/Iceman2050/header-hunter">header-hunter</a>
(one request per site, timeouts, redirect caps). "Suspicious" means
<em>possible</em> indirect prompt injection — unconfirmed by definition; this
dataset never claims confirmed attacks. v0.1 covers 44 well-known sites; it is a
seed, not a census. Failed scans are kept in the dataset with their error.
</div>

<h2>Get the data</h2>
<p><a href="../dataset/@@DSFILE@@" download>Download observations JSON</a> |
<a href="https://github.com/Iceman2050/agent-headers-observatory">GitHub repo</a> |
<a href="https://github.com/Iceman2050/agent-headers-observatory/blob/main/CONTRIBUTING.md">Contribute your scans</a></p>

<h2>Roadmap</h2>
<ul>
<li>Weekly re-scans with per-site trend lines</li>
<li>HTTP API for the dataset</li>
<li>Suspicious-header alert feed</li>
</ul>

<footer>Agent Headers Observatory | MIT licensed | by Ingenious AI |
numbers generated from the dataset, never hand-typed.</footer>
</body>
</html>
"""


def main() -> int:
    s = compute()
    ds = json.loads((ROOT / "dataset" / s["dataset_file"]).read_text())
    interesting = [o for o in ds["observations"] if o["headers_of_interest"]]

    rows = "\n".join(
        "<tr><td><code>%s</code></td><td>%s</td><td><code>%s</code></td>"
        "<td>%s</td></tr>"
        % (
            html.escape(o["url"]),
            html.escape(o["verdict"]),
            html.escape(o["headers_of_interest"][0]["header"]),
            html.escape(o["headers_of_interest"][0]["value"][:100]),
        )
        for o in interesting
    ) or '<tr><td colspan="4">No agent-directed or suspicious headers observed yet.</td></tr>'

    top = "\n".join(
        "<tr><td><code>%s</code></td><td>%d</td></tr>" % (html.escape(n), c)
        for n, c in s["top_header_names"]
    ) or "<tr><td colspan=\"2\">—</td></tr>"

    tokens = {
        "@@SITES@@": str(s["sites_observed"]),
        "@@AD@@": str(s["agent_directed"]),
        "@@SUSP@@": str(s["suspicious"]),
        "@@ERR@@": str(s["errors"]),
        "@@DSFILE@@": html.escape(s["dataset_file"]),
        "@@GEN@@": html.escape(str(s["generated_at"])),
        "@@SCHEMA@@": html.escape(str(s["schema_version"])),
        "@@ROWS@@": rows,
        "@@TOP@@": top,
    }
    page = TEMPLATE
    for k, v in tokens.items():
        page = page.replace(k, v)
    assert "@@" not in page, "unreplaced token remains"
    (ROOT / "site" / "index.html").write_text(page)
    print("wrote site/index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
