from __future__ import annotations

from typing import TYPE_CHECKING
import humanize
import datetime
import discord
from discord.ext import commands
import inspect
import os

if TYPE_CHECKING:
    from bot import RoboAy


class Misc(commands.Cog):
    def __init__(self, bot: RoboAy) -> None:
        self.bot = bot 


    @commands.command(name="echo", aliases=["say"])
    async def _echo(self, ctx: commands.Context, msg: str):
        await ctx.send(msg)


    @commands.command(name="ping")
    async def _ping(self, ctx: commands.Context):
        await ctx.send(embed=discord.Embed(title="Pong!", description=f"{self.bot.latency*1000:.2f} ms"))


    @commands.command(name="uptime")
    async def _uptime(self, ctx: commands.Context):
        await ctx.send(f"I have been up for {humanize.precisedelta(datetime.datetime.utcnow() - self.bot.uptime, format ='%0.2f')}")


    @commands.command(name="source")
    async def source(self, ctx: commands.Context, command: str = None):
        if command is None:
            return await ctx.send('<https://github.com/Ay-355/RoboAy355>')
        if (obj := self.bot.get_command(command.replace('.', ' '))) is None:
            return await ctx.send(f'Could not find command `{command}`')

        _code = obj.callback.__code__
        module = obj.callback.__module__
        filename = _code.co_filename

        lines, firstlineno = inspect.getsourcelines(_code)
        if not module.startswith('discord'):
            location = os.path.relpath(filename).replace('\\', '/')

        await ctx.send(f"Here is the source for the `{command}` command -> <https://github.com/Ay-355/RoboAy355/blob/master/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>")



def setup(bot: RoboAy):
    bot.add_cog(Misc(bot))
