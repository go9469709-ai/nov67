"""Cog de sistema de níveis."""
from __future__ import annotations
import discord
from discord.ext import commands
from config import config

class Levels(commands.Cog):
    """Sistema de XP e níveis."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        guild_config = await self.bot.db.get_guild(message.guild.id)
        if not guild_config["xp_enabled"]:
            return
        data = await self.bot.db.get_member(message.guild.id, message.author.id)
        new_xp = data["xp"] + config.xp_per_message
        level_xp = config.level_up_base * (config.level_up_mult ** data["level"])
        if new_xp >= level_xp:
            new_level = data["level"] + 1
            new_xp -= int(level_xp)
            await self.bot.db.update_member(message.guild.id, message.author.id, xp=new_xp, level=new_level)
            level_up_msg = guild_config["level_up_msg"].format(user=message.author.mention, level=new_level)
            await message.channel.send(level_up_msg)
        else:
            await self.bot.db.update_member(message.guild.id, message.author.id, xp=new_xp)

    @commands.command(name="rank")
    async def rank(self, ctx: commands.Context, member: discord.Member = None):
        """Mostra o rank de um membro."""
        target = member or ctx.author
        data = await self.bot.db.get_member(ctx.guild.id, target.id)
        level = data["level"]
        xp = data["xp"]
        level_xp = int(config.level_up_base * (config.level_up_mult ** level))
        embed = discord.Embed(title=f"Rank de {target}", color=0x5865F2)
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="📊 Nível", value=str(level), inline=True)
        embed.add_field(name="⭐ XP", value=f"{xp}/{level_xp}", inline=True)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Levels(bot))