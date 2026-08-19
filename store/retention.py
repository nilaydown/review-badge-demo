"""Retention helpers for the artifact store."""

import os
import time

WINDOW_DAYS = 30


def expired(items, now=None):
    now = now or time.time()
    return [i for i in items if now - i["created_at"] > WINDOW_DAYS * 86400]
