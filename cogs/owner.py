from __future__ import annotations

from typing import TYPE_CHECKING
import traceback

import discord
from discord.ext import commands
from utils.context import RContext

if TYPE_CHECKING:
    from bot import RoboAy



class Owner(commands.Cog):
    def __init__(self, bot: RoboAy) -> None:
        self.bot = bot

    def cog_check(self, ctx: RContext):
        if ctx.author.id in self.bot.owner_ids:
            return True
        raise commands.NotOwner()


    @commands.command(name="reload", aliases=["r"])
    async def reload(self, ctx: RContext, cog: str):
        if cog in {"a", "all"}:
            m = ""
            for ext in list(self.bot.extensions):
                try:
                    self.bot.reload_extension(ext)
                    m += f"Reloaded {ext}\n"
                except Exception as e:
                    await ctx.send(e)
                    traceback.print_exc()
            await ctx.send(m)
            return await ctx.done()
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Reloaded {cog}")
            await ctx.done()
        except Exception as e:
            await ctx.send(e)


    @commands.command(name="unload", aliases=["u"])
    async def unload(self, ctx: RContext, cog: str):
        if cog in {"a", "all"}:
            for ext in list(self.bot.extensions):
                try:
                    self.bot.unload_extension(ext)
                    await ctx.send(f"Done")
                except Exception as e:
                    await ctx.send(e)
                    traceback.print_exc()
        else:
            try:
                self.bot.unload_extension(f"cogs.{cog}")
                await ctx.done()
            except Exception as e:
                await ctx.send(e)



    @commands.command(name="load", aliases=["l"])
    async def load(self, ctx: RContext, cog: str):
        if cog in {"a", "all"}:
            for ext in list(self.bot.extensions):
                try:
                    self.bot.load_extension(ext)
                    await ctx.send(f"Done")
                except Exception as e:
                    await ctx.send(e)
                    traceback.print_exc()
            return await ctx.done()
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.done()
        except Exception as e:
            await ctx.send(e)


def setup(bot: RoboAy):
    bot.add_cog(Owner(bot))
