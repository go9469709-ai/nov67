"""Cog de IA."""
from __future__ import annotations
import discord
from discord.ext import commands
from utils.embeds import error as embed_error, success as embed_success

class AI(commands.Cog):
    """Interação com IA."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ai")
    async def ai_command(self, ctx: commands.Context, *, query: str):
        """Faz uma pergunta para a IA."""
        async with ctx.typing():
            try:
                response = "IA em desenvolvimento. Configure sua API OpenAI no .env"
                embed = discord.Embed(title="NovaEra IA", description=response, color=0x5865F2)
                embed.set_author(name=f"{ctx.author} perguntou:")
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(embed=embed_error("Erro", str(e)))

async def setup(bot: commands.Bot):
    await bot.add_cog(AI(bot))