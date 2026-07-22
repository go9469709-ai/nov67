"""Cog de música (placeholder)."""
from __future__ import annotations
import discord
from discord.ext import commands

class Music(commands.Cog):
    """Sistema de música (em desenvolvimento)."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, query: str):
        """Toca uma música."""
        await ctx.send("🎵 Sistema de música em desenvolvimento.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))