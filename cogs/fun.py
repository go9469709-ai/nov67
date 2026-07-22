"""Cog de diversão."""
from __future__ import annotations
import random
import discord
from discord.ext import commands

class Fun(commands.Cog):
    """Comandos divertidos."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def eightball(self, ctx: commands.Context, *, question: str):
        """Pergunta mágica para a bola 8."""
        responses = [
            "Sim!", "Não!", "Talvez...", "Definitivamente!", "Nunca!",
            "Pergunte novamente mais tarde.", "Sem dúvida.", "Não há chance."
        ]
        embed = discord.Embed(title="🎱 Bola Mágica", description=random.choice(responses), color=0x5865F2)
        await ctx.send(embed=embed)

    @commands.command(name="dice")
    async def dice(self, ctx: commands.Context, sides: int = 6):
        """Rola um dado."""
        result = random.randint(1, sides)
        embed = discord.Embed(title="🎲 Dado", description=f"Você rolou: **{result}**", color=0x5865F2)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))