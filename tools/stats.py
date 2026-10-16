#!/usr/bin/env python3
"""Compute aggregate stats FROM the dataset file. Never hand-type numbers
onto the site — run this and paste/emit its output instead.

Usage: python3 tools/stats.py [--json]   (run from the repo root)
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DS = sorted((ROOT / "dataset").glob("observations-*.json"))[-1]


def compute() -> dict:
    ds = json.loads(DS.read_text())
    obs = ds["observations"]
    verdicts = Counter(o["verdict"] for o in obs)
    header_names = Counter()
    for o in obs:
        for h in o["headers_of_interest"]:
            header_names[h["header"].lower()] += 1
    errors = sum(1 for o in obs if o["error"])
    return {
        "dataset_file": DS.name,
        "schema_version": ds.get("schema_version"),
        "generated_at": ds.get("generated_at"),
        "sites_observed": len(obs),
        "verdicts": dict(verdicts),
        "agent_directed": sum(
            1 for o in obs
            if any(h["category"] == "agent-directed"
                   for h in o["headers_of_interest"])),
        "suspicious": sum(
            1 for o in obs
            if any(h["category"] == "suspicious"
                   for h in o["headers_of_interest"])),
        "errors": errors,
        "top_header_names": header_names.most_common(15),
    }


def main() -> int:
    stats = compute()
    if "--json" in sys.argv:
        print(json.dumps(stats, indent=2))
    else:
        print(f"dataset:            {stats['dataset_file']}")
        print(f"sites observed:     {stats['sites_observed']}")
        print(f"agent-directed:     {stats['agent_directed']}")
        print(f"suspicious:         {stats['suspicious']}")
        print(f"errors:             {stats['errors']}")
        print("verdicts:", stats["verdicts"])
        print("top header names:")
        for name, n in stats["top_header_names"]:
            print(f"  {name}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
