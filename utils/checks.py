"""Verificações de permissão para comandos."""
from __future__ import annotations
import discord
from discord.ext import commands
from config import config

def is_owner():
    async def predicate(ctx):
        if ctx.author.id == config.owner_id:
            return True
        raise commands.NotOwner
    return commands.check(predicate)

def has_guild_perms(**perms):
    return commands.has_guild_permissions(**perms)

def is_admin():
    return commands.has_guild_permissions(administrator=True)

def is_mod():
    return commands.has_guild_permissions(
        manage_messages=True, kick_members=True, ban_members=True
    )