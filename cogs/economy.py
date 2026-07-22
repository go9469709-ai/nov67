"""Cog de economia."""
from __future__ import annotations
import random
import discord
from discord.ext import commands
from config import config
from utils.embeds import success as embed_success, error as embed_error

class Economy(commands.Cog):
    """Sistema de economia com moeda virtual."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx: commands.Context, member: discord.Member = None):
        """Mostra o saldo de um membro."""
        target = member or ctx.author
        data = await self.bot.db.get_member(ctx.guild.id, target.id)
        balance = data["balance"]
        bank = data["bank"]
        total = balance + bank
        embed = discord.Embed(title=f"Carteira de {target}", color=0x5865F2)
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="💵 Em mão", value=f"R${balance:,}", inline=True)
        embed.add_field(name="🏦 No banco", value=f"R${bank:,}", inline=True)
        embed.add_field(name="💰 Total", value=f"R${total:,}", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="daily")
    @commands.cooldown(1, config.daily_cooldown, commands.BucketType.user)
    async def daily(self, ctx: commands.Context):
        """Recebe sua recompensa diária."""
        data = await self.bot.db.get_member(ctx.guild.id, ctx.author.id)
        await self.bot.db.update_member(ctx.guild.id, ctx.author.id, balance=data["balance"] + config.daily_amount)
        embed = embed_success("Daily Recebido", f"Você recebeu **R${config.daily_amount:,}**")
        await ctx.send(embed=embed)

    @commands.command(name="work")
    @commands.cooldown(1, config.work_cooldown, commands.BucketType.user)
    async def work(self, ctx: commands.Context):
        """Trabalha para ganhar dinheiro."""
        amount = random.randint(config.work_min, config.work_max)
        data = await self.bot.db.get_member(ctx.guild.id, ctx.author.id)
        await self.bot.db.update_member(ctx.guild.id, ctx.author.id, balance=data["balance"] + amount)
        embed = embed_success("Trabalho Concluído", f"Você ganhou **R${amount:,}**")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))