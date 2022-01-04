from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord
from discord import ui
from discord.ext import commands
from utils.context import RContext

if TYPE_CHECKING:
    from bot import RoboAy


class Selects(commands.Cog):
    def __init__(self, bot: RoboAy) -> None:
        self.bot = bot


    @commands.command(name="poll")
    async def poll(self, ctx: RContext, *, options):
        """Create a select menu poll. For multiple options, split your arguments with a |. 
        Example: poll foo | bar baz | foobar"""
        ...


def setup(bot: RoboAy):
    bot.add_cog(Selects(bot))
