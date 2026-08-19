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
