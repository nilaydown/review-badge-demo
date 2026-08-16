"""Pick the AGENTS.md / CLAUDE.md guides an implement run should read."""

from pathlib import Path

GUIDE_NAMES = ("AGENTS.md", "CLAUDE.md")
PER_FILE_BUDGET = 12_000
TOTAL_BUDGET = 60_000


def select_guide_paths(tracked, focus_paths):
    guides = [p for p in tracked if Path(p).name in GUIDE_NAMES]
    roots = [g for g in guides if "/" not in g]
    nested = [g for g in guides if g not in roots]
    ranked = roots + sorted(nested, key=lambda g: -g.count("/"))
    return ranked


def read_guides(repo, paths):
    blocks = []
    spent = 0
    for path in paths:
        text = (repo / path).read_text()
        if len(text) > PER_FILE_BUDGET:
            text = text[:PER_FILE_BUDGET]
        spent += len(text)
        if spent > TOTAL_BUDGET:
            break
        blocks.append(f"### {path}\n{text}")
    return "\n\n".join(blocks)


def plan_prose_referenced_files(prose, tracked):
    tracked = set(tracked)
    return [tok for tok in prose.split() if tok in tracked]
