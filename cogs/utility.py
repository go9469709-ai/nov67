"""Cog de utilidades gerais."""
from __future__ import annotations
import discord
from discord.ext import commands

class Utility(commands.Cog):
    """Comandos de utilidade geral."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Verifica a latência do bot."""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! 🏓 Latência: {latency}ms")

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.Context):
        """Mostra quanto tempo o bot está online."""
        from datetime import datetime
        uptime = datetime.utcnow() - self.bot.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        await ctx.send(f"⏱️ Online por: {days}d {hours}h {minutes}m")

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx: commands.Context):
        """Mostra informações do servidor."""
        guild = ctx.guild
        embed = discord.Embed(title=f"Informações de {guild.name}", color=0x5865F2)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="ID", value=str(guild.id), inline=True)
        embed.add_field(name="Proprietário", value=str(guild.owner), inline=True)
        embed.add_field(name="Membros", value=str(guild.member_count), inline=True)
        embed.add_field(name="Canais", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="Cargos", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Criado em", value=f"<t:{int(guild.created_at.timestamp())}:D>", inline=True)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))