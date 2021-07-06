from __future__ import annotations

from typing import TYPE_CHECKING
import discord
from discord.ext import commands
# from discord_slash import cog_ext, SlashContext

if TYPE_CHECKING:
    from bot import RoboAy



#! bad

# class SlashCmds(commands.Cog):
#     def __init__(self, bot: RoboAy):
#         self.bot = bot


#     @cog_ext.cog_slash(name="test")
#     async def test(self, ctx: SlashContext):
#         """A test slash command"""
#         await ctx.send(content="this is a test message")


#     @cog_ext.cog_slash(name="ping")
#     async def ping(self, ctx: SlashContext):
#         """Sends the latency of the bot, but it's in a slash command"""
#         await ctx.send(content=f"Pong! {self.bot.latency*1000:.2f} ms")


# def setup(bot: RoboAy):
#     bot.add_cog(SlashCmds(bot))
