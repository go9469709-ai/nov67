"""Cog de sistema de tickets."""
from __future__ import annotations
import discord
from discord.ext import commands

class Tickets(commands.Cog):
    """Sistema de tickets de suporte."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ticket")
    async def ticket(self, ctx: commands.Context):
        """Cria um novo ticket."""
        guild_config = await self.bot.db.get_guild(ctx.guild.id)
        category_id = guild_config["tickets_category"]
        if not category_id:
            await ctx.send("❌ Categoria de tickets não configurada.")
            return
        category = ctx.guild.get_channel(category_id)
        if not category:
            await ctx.send("❌ Categoria não encontrada.")
            return
        ticket_channel = await category.create_text_channel(name=f"ticket-{ctx.author.id}")
        embed = discord.Embed(title="Novo Ticket", description=f"Ticket criado por {ctx.author.mention}", color=0x5865F2)
        await ticket_channel.send(embed=embed)
        await ctx.send(f"✅ Ticket criado: {ticket_channel.mention}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))