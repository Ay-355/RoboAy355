from __future__ import annotations

from typing import TYPE_CHECKING
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

if TYPE_CHECKING:
    from bot import RoboAy




class SlashCmds(commands.Cog):
    def __init__(self, bot: RoboAy):
        self.bot = bot


    @cog_ext.cog_slash(name="test")
    async def ping(self, ctx: SlashContext):
        await ctx.send(content="this is a test")


    @cog_ext.cog_slash(name="pog")
    async def pog(self, ctx: SlashContext):
        await ctx.send(content="pog")


def setup(bot: RoboAy):
    bot.add_cog(SlashCmds(bot))
