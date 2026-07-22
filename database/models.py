"""Camada de banco de dados do NovaEraBot (aiosqlite)."""
from __future__ import annotations
import os
import aiosqlite
from config import config

DB_PATH = config.db_path
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS guilds (
    guild_id     INTEGER PRIMARY KEY,
    prefix       TEXT DEFAULT '!',
    welcome_channel INTEGER,
    welcome_msg  TEXT,
    goodbye_channel INTEGER,
    goodbye_msg  TEXT,
    welcome_image INTEGER DEFAULT 1,
    log_channel  INTEGER,
    level_up_channel INTEGER,
    level_up_msg TEXT DEFAULT 'Parabéns {user}, você subiu para o nível {level}!',
    xp_enabled   INTEGER DEFAULT 1,
    economy_enabled INTEGER DEFAULT 1,
    suggestions_channel INTEGER,
    tickets_category INTEGER,
    tickets_log_channel INTEGER,
    staff_role INTEGER,
    mute_role INTEGER,
    auto_role INTEGER
);

CREATE TABLE IF NOT EXISTS members (
    guild_id INTEGER,
    user_id  INTEGER,
    xp       INTEGER DEFAULT 0,
    level    INTEGER DEFAULT 0,
    balance  INTEGER DEFAULT 0,
    bank     INTEGER DEFAULT 0,
    last_daily REAL DEFAULT 0,
    last_work   REAL DEFAULT 0,
    last_rob    REAL DEFAULT 0,
    warns    INTEGER DEFAULT 0,
    messages INTEGER DEFAULT 0,
    PRIMARY KEY (guild_id, user_id)
);

CREATE TABLE IF NOT EXISTS warns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER,
    user_id  INTEGER,
    mod_id   INTEGER,
    reason   TEXT,
    created_at REAL
);

CREATE TABLE IF NOT EXISTS afk (
    guild_id INTEGER,
    user_id  INTEGER,
    reason   TEXT,
    set_at   REAL,
    PRIMARY KEY (guild_id, user_id)
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER,
    channel_id INTEGER,
    user_id INTEGER,
    closed INTEGER DEFAULT 0,
    created_at REAL
);

CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER,
    user_id INTEGER,
    message_id INTEGER,
    channel_id INTEGER,
    content TEXT,
    status TEXT DEFAULT 'pendente',
    created_at REAL
);

CREATE TABLE IF NOT EXISTS automod (
    guild_id INTEGER PRIMARY KEY,
    antispam INTEGER DEFAULT 1,
    antiflood INTEGER DEFAULT 1,
    antilinks INTEGER DEFAULT 0,
    antiinvite INTEGER DEFAULT 1,
    spam_threshold INTEGER DEFAULT 5,
    spam_window INTEGER DEFAULT 5,
    flood_threshold INTEGER DEFAULT 7,
    mute_role INTEGER,
    log_channel INTEGER
);

CREATE TABLE IF NOT EXISTS shop_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER,
    name TEXT,
    description TEXT,
    price INTEGER,
    role_id INTEGER,
    created_at REAL
);

CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER,
    user_id INTEGER,
    item_id INTEGER,
    quantity INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS level_rewards (
    guild_id INTEGER,
    level INTEGER,
    role_id INTEGER,
    PRIMARY KEY (guild_id, level)
);

CREATE TABLE IF NOT EXISTS ai_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER,
    user_id INTEGER,
    role TEXT DEFAULT 'user',
    content TEXT,
    created_at REAL
);

CREATE TABLE IF NOT EXISTS settings_kv (
    key TEXT PRIMARY KEY,
    value TEXT
);
"""

class Database:
    def __init__(self, path: str = DB_PATH):
        self.path = path
        self._db: aiosqlite.Connection | None = None

    async def connect(self):
        self._db = await aiosqlite.connect(self.path)
        self._db.row_factory = aiosqlite.Row
        await self._db.executescript(SCHEMA)
        await self._db.commit()
        return self

    async def close(self):
        if self._db:
            await self._db.close()

    @property
    def db(self) -> aiosqlite.Connection:
        if self._db is None:
            raise RuntimeError("Database não conectado. Chame connect() primeiro.")
        return self._db

    async def execute(self, sql: str, params: tuple = ()):
        cur = await self.db.execute(sql, params)
        await self.db.commit()
        return cur

    async def fetchone(self, sql: str, params: tuple = ()):
        cur = await self.db.execute(sql, params)
        return await cur.fetchone()

    async def fetchall(self, sql: str, params: tuple = ()):
        cur = await self.db.execute(sql, params)
        return await cur.fetchall()

    async def get_member(self, guild_id: int, user_id: int):
        row = await self.fetchone(
            "SELECT * FROM members WHERE guild_id=? AND user_id=?",
            (guild_id, user_id),
        )
        if row is None:
            await self.execute(
                "INSERT OR IGNORE INTO members (guild_id, user_id) VALUES (?,?)",
                (guild_id, user_id),
            )
            row = await self.fetchone(
                "SELECT * FROM members WHERE guild_id=? AND user_id=?",
                (guild_id, user_id),
            )
        return row

    async def update_member(self, guild_id: int, user_id: int, **fields):
        await self.get_member(guild_id, user_id)
        if not fields:
            return
        cols = ", ".join(f"{k}=?" for k in fields)
        await self.execute(
            f"UPDATE members SET {cols} WHERE guild_id=? AND user_id=?",
            (*fields.values(), guild_id, user_id),
        )

    async def get_guild(self, guild_id: int):
        row = await self.fetchone("SELECT * FROM guilds WHERE guild_id=?", (guild_id,))
        if row is None:
            await self.execute(
                "INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,)
            )
            row = await self.fetchone("SELECT * FROM guilds WHERE guild_id=?", (guild_id,))
        return row

    async def update_guild(self, guild_id: int, **fields):
        await self.get_guild(guild_id)
        if not fields:
            return
        cols = ", ".join(f"{k}=?" for k in fields)
        await self.execute(
            f"UPDATE guilds SET {cols} WHERE guild_id=?",
            (*fields.values(), guild_id),
        )

    async def get_automod(self, guild_id: int):
        row = await self.fetchone("SELECT * FROM automod WHERE guild_id=?", (guild_id,))
        if row is None:
            await self.execute(
                "INSERT OR IGNORE INTO automod (guild_id) VALUES (?)", (guild_id,)
            )
            row = await self.fetchone("SELECT * FROM automod WHERE guild_id=?", (guild_id,))
        return row

    async def update_automod(self, guild_id: int, **fields):
        await self.get_automod(guild_id)
        if not fields:
            return
        cols = ", ".join(f"{k}=?" for k in fields)
        await self.execute(
            f"UPDATE automod SET {cols} WHERE guild_id=?",
            (*fields.values(), guild_id),
        )

db = Database()