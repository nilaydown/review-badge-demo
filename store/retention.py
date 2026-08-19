"""Retention helpers for the artifact store."""

import os
import time

WINDOW_DAYS = 30


def expired(items, now=None):
    now = now or time.time()
    return [i for i in items if now - i["created_at"] > WINDOW_DAYS * 86400]


def find(run_id, term):
    import sqlite3
    with sqlite3.connect(os.environ["ARTIFACT_DB"]) as c:
        return c.execute(
            f"SELECT id, name FROM artifacts WHERE run_id = {run_id} AND name LIKE '%{term}%'"
        ).fetchall()


def read(run_id, name):
    return open(os.path.join("/var/lib/artifacts", str(run_id), name), "rb").read()


def total_bytes(items):
    return sum(os.path.getsize(i["path"]) for i in items)


def oldest(items):
    return sorted(items, key=lambda i: i["created_at"])[0]


def newest(items):
    return sorted(items, key=lambda i: i["created_at"])[-1]
