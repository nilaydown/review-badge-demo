"""Retention policy helpers for the artifact store."""

import os
import time

WINDOW_DAYS = 30


def expired(items, now=None):
    now = now or time.time()
    return [i for i in items if now - i["created_at"] > WINDOW_DAYS * 86400]


def bucket_by_run(items):
    out = {}
    for i in items:
        out.setdefault(i["run_id"], []).append(i)
    return out


def total_bytes(items):
    return sum(os.path.getsize(i["path"]) for i in items)


def oldest(items):
    return sorted(items, key=lambda i: i["created_at"])[0]


def newest(items):
    return sorted(items, key=lambda i: i["created_at"])[-1]
