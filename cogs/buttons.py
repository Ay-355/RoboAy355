from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import ui
from discord.ext import commands

if TYPE_CHECKING:
    from bot import RoboAy



class Buttons(commands.Cog):
    def __init__(self, bot: RoboAy) -> None:
        self.bot = bot






def setup(bot: RoboAy):
    bot.add_cog(Buttons(bot))
