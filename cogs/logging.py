"""Cog de logging de eventos."""
from __future__ import annotations
import discord
from discord.ext import commands

class Logging(commands.Cog):
    """Registro de eventos do servidor."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        guild_config = await self.bot.db.get_guild(message.guild.id)
        log_channel_id = guild_config["log_channel"]
        if not log_channel_id:
            return
        channel = message.guild.get_channel(log_channel_id)
        if not channel:
            return
        embed = discord.Embed(title="Mensagem Deletada", color=0xFF0000)
        embed.add_field(name="Autor", value=str(message.author), inline=True)
        embed.add_field(name="Canal", value=message.channel.mention, inline=True)
        embed.add_field(name="Conteúdo", value=message.content[:1024], inline=False)
        await channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Logging(bot))