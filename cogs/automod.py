"""Cog de auto-moderação."""
from __future__ import annotations
import discord
from discord.ext import commands
from utils.helpers import has_invites, has_links

class AutoMod(commands.Cog):
    """Sistema automático de moderação."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        guild = message.guild
        if not guild:
            return
        automod = await self.bot.db.get_automod(guild.id)
        if automod["antiinvite"] and has_invites(message.content):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Convites não são permitidos aqui.", delete_after=5)
            except Exception:
                pass
        elif automod["antilinks"] and has_links(message.content):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Links não são permitidos aqui.", delete_after=5)
            except Exception:
                pass

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoMod(bot))