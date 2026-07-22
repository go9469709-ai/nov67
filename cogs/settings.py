"""Cog de configurações do servidor."""
from __future__ import annotations
import discord
from discord.ext import commands
from utils.embeds import success as embed_success, error as embed_error

class Settings(commands.Cog):
    """Configurações do servidor."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="setprefix")
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: commands.Context, prefix: str):
        """Define o prefixo do bot no servidor."""
        await self.bot.db.update_guild(ctx.guild.id, prefix=prefix)
        await ctx.send(embed=embed_success("Prefixo Alterado", f"Novo prefixo: `{prefix}`"))

    @commands.command(name="setwelcome")
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx: commands.Context, channel: discord.TextChannel, *, message: str):
        """Define o canal e a mensagem de boas-vindas."""
        await self.bot.db.update_guild(ctx.guild.id, welcome_channel=channel.id, welcome_msg=message)
        await ctx.send(embed=embed_success("Boas-vindas Configuradas", f"Canal: {channel.mention}"))

async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))