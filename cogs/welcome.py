"""Cog de boas-vindas."""
from __future__ import annotations
import discord
from discord.ext import commands

class Welcome(commands.Cog):
    """Mensagens de boas-vindas."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_config = await self.bot.db.get_guild(member.guild.id)
        welcome_channel_id = guild_config["welcome_channel"]
        if not welcome_channel_id:
            return
        channel = member.guild.get_channel(welcome_channel_id)
        if not channel:
            return
        welcome_msg = guild_config["welcome_msg"] or f"Bem-vindo, {member.mention}!"
        embed = discord.Embed(title="Bem-vindo!", description=welcome_msg, color=0x5865F2)
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))