"""Cog de moderação."""
from __future__ import annotations
from datetime import timedelta
import discord
from discord.ext import commands
from utils.embeds import error as embed_error, success as embed_success

class Moderation(commands.Cog):
    """Comandos de moderação."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Sem motivo"):
        """Bane um membro do servidor."""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send(embed=embed_error("Erro", "Você não pode banir este membro."))
            return
        try:
            await member.ban(reason=reason)
            embed = embed_success("Membro Banido", f"{member} foi banido.\nMotivo: {reason}")
            embed.set_thumbnail(url=member.display_avatar.url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=embed_error("Erro", str(e)))

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = "Sem motivo"):
        """Expulsa um membro do servidor."""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send(embed=embed_error("Erro", "Você não pode expulsar este membro."))
            return
        try:
            await member.kick(reason=reason)
            embed = embed_success("Membro Expulso", f"{member} foi expulso.\nMotivo: {reason}")
            embed.set_thumbnail(url=member.display_avatar.url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=embed_error("Erro", str(e)))

    @commands.command(name="timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx: commands.Context, member: discord.Member, minutes: int = 10, *, reason: str = "Sem motivo"):
        """Silencia um membro temporariamente."""
        try:
            await member.timeout(timedelta(minutes=minutes), reason=reason)
            embed = embed_success("Membro Silenciado", f"{member} foi silenciado por {minutes} minutos.\nMotivo: {reason}")
            embed.set_thumbnail(url=member.display_avatar.url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=embed_error("Erro", str(e)))

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int = 10):
        """Apaga mensagens do canal."""
        try:
            deleted = await ctx.channel.purge(limit=amount)
            embed = embed_success("Mensagens Apagadas", f"{len(deleted)} mensagem(s) foram apagadas.")
            msg = await ctx.send(embed=embed)
            await msg.delete(delay=5)
        except Exception as e:
            await ctx.send(embed=embed_error("Erro", str(e)))

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))