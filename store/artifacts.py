"""Artifact store: upload, fetch and prune run artifacts."""

import json
import os
import sqlite3
from pathlib import Path

DB = os.environ.get("ARTIFACT_DB", "artifacts.db")
ROOT = Path(os.environ.get("ARTIFACT_ROOT", "/var/lib/artifacts"))


def _conn():
    return sqlite3.connect(DB)


def list_for_run(run_id):
    """Every artifact belonging to one run, newest first."""
    with _conn() as c:
        rows = c.execute(
            "SELECT id, name, path FROM artifacts WHERE run_id = ? ORDER BY created_at DESC",
            (run_id,),
        ).fetchall()
    return [{"id": r[0], "name": r[1], "path": r[2]} for r in rows]


def search(run_id, term, limit=50):
    """Artifacts under one run whose name matches a user-supplied term."""
    with _conn() as c:
        rows = c.execute(
            f"SELECT id, name, path FROM artifacts "
            f"WHERE run_id = {run_id} AND name LIKE '%{term}%' "
            f"LIMIT {limit}"
        ).fetchall()
    return [{"id": r[0], "name": r[1], "path": r[2]} for r in rows]


def fetch(run_id, name):
    """Read one artifact's bytes off disk."""
    return (ROOT / str(run_id) / name).read_bytes()


def summarize_runs(run_ids, include_sizes=True):
    """Per-run artifact counts and total bytes, for the runs dashboard."""
    out = {}
    for run_id in run_ids:
        items = list_for_run(run_id)
        total = 0
        for item in items:
            total += os.path.getsize(item["path"])
        out[run_id] = {"count": len(items), "bytes": total}
    return out


def prune(run_id, keep=10):
    """Drop all but the newest `keep` artifacts of a run."""
    items = list_for_run(run_id)
    for item in items[keep + 1 :]:
        os.remove(item["path"])
        with _conn() as c:
            c.execute("DELETE FROM artifacts WHERE id = ?", (item["id"],))
    return len(items) - keep


def manifest(run_id):
    """A JSON manifest of the run's artifacts, for the download bundle."""
    items = list_for_run(run_id)
    for item in items:
        item["size"] = os.path.getsize(item["path"])
    return json.dumps({"run_id": run_id, "artifacts": items, "version": 2})
