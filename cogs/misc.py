from __future__ import annotations

from typing import TYPE_CHECKING
import humanize
import datetime
import discord
from discord.ext import commands
import inspect
import os
from utils.context import RContext


if TYPE_CHECKING:
    from bot import RoboAy


class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        self.query = query.replace(' ', '+')

        self.google_button = discord.ui.Button(style=discord.ButtonStyle.link, label='Click Here', url='https://www.google.com/search?q=' + self.query)

        self.add_item(self.google_button)


class Misc(commands.Cog):
    def __init__(self, bot: RoboAy) -> None:
        self.bot = bot 


    @commands.command(name="echo", aliases=["say"])
    async def _echo(self, ctx: RContext, msg: str):
        """Input a message and get it repeated"""
        await ctx.send(msg)
        await ctx.done()


    @commands.command(name="ping")
    async def _ping(self, ctx: RContext):
        """See the latency of the bot"""
        await ctx.send(embed=discord.Embed(title="Pong!", description=f"{self.bot.latency*1000:.2f} ms"))
        await ctx.done()


    @commands.command(name="uptime")
    async def _uptime(self, ctx: RContext):
        """See how long the bot has been up for"""
        await ctx.send(f"I have been up for {humanize.precisedelta(datetime.datetime.utcnow() - self.bot.uptime, format ='%0.2f')}")
        await ctx.done()


    @commands.command(name="source")
    async def source(self, ctx: RContext, command: str = None): #taken from R.Danny: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L344-L382
        """Sends the repo link or the link to the source of a command"""
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
        await ctx.done()


    @commands.command(name="google")
    async def google(self, ctx: RContext, *, query: str):
        """Returns a google link for your query"""
        await ctx.send(f"Google Result for: `{query}`", view=Google(query))



def setup(bot: RoboAy):
    bot.add_cog(Misc(bot))
