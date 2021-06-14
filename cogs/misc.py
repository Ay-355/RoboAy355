from __future__ import annotations

from typing import TYPE_CHECKING
import discord
from discord.ext import commands

if TYPE_CHECKING:
    from bot import RoboAy


class Misc(commands.Cog):
    def __init__(self, bot: RoboAy):
        self.bot = bot 


    @commands.command(name="ping")
    async def _ping(self, ctx: commands.Context):
        await ctx.send(embed=discord.Embed(title="Pong!", description=f"{self.bot.latency*1000:.2f} ms"))


def setup(bot: RoboAy):
    bot.add_cog(Misc(bot))
