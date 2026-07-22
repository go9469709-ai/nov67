"""Funções utilitárias compartilhadas."""
from __future__ import annotations
import re
import time
import asyncio
import functools
from typing import Iterable

URL_REGEX = re.compile(r"https?://\S+", re.IGNORECASE)
INVITE_REGEX = re.compile(r"(discord\.gg|discord(app)?\.com/invite)/\S+", re.IGNORECASE)

def now() -> float:
    return time.time()

def format_seconds(seconds: float) -> str:
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    if seconds < 86400:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}m"
    return f"{seconds // 86400}d {(seconds % 86400) // 3600}h"

def has_links(text: str) -> bool:
    return bool(URL_REGEX.search(text))

def has_invites(text: str) -> bool:
    return bool(INVITE_REGEX.search(text))

def cooldown_left(last: float, cooldown: float) -> float:
    elapsed = now() - last
    return max(0.0, cooldown - elapsed)

def chunk(seq: list, size: int) -> Iterable[list]:
    for i in range(0, len(seq), size):
        yield seq[i : i + size]

async def to_thread(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, functools.partial(func, *args, **kwargs)
    )