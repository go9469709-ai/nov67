"""Cog de comandos do dono."""
from __future__ import annotations
import discord
from discord.ext import commands
from utils.checks import is_owner

class Owner(commands.Cog):
    """Comandos restritos ao dono do bot."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="load")
    @is_owner()
    async def load(self, ctx: commands.Context, cog: str):
        """Carrega um cog."""
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Cog `{cog}` carregado.")
        except Exception as e:
            await ctx.send(f"❌ Erro: {e}")

    @commands.command(name="unload")
    @is_owner()
    async def unload(self, ctx: commands.Context, cog: str):
        """Descarrega um cog."""
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Cog `{cog}` descarregado.")
        except Exception as e:
            await ctx.send(f"❌ Erro: {e}")

    @commands.command(name="reload")
    @is_owner()
    async def reload(self, ctx: commands.Context, cog: str):
        """Recarrega um cog."""
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Cog `{cog}` recarregado.")
        except Exception as e:
            await ctx.send(f"❌ Erro: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Owner(bot))