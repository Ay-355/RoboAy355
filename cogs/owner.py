from __future__ import annotations

from typing import TYPE_CHECKING
import traceback

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from bot import RoboAy



class Owner(commands.Cog):
    def __init__(self, bot: RoboAy) -> None:
        self.bot = bot


    @commands.command(name="reload", aliases=["r"])
    async def reload(self, ctx: commands.Context, cog: str):
        if cog in {"a", "all"}:
            for ext in list(self.bot.extensions):
                try:
                    self.bot.reload_extension(ext)
                    await ctx.send(f"Done, reloaded {ext}")
                except Exception as e:
                    await ctx.send(e)
                    traceback.print_exc()
        else:
            try:
                self.bot.reload_extension(f"cogs.{cog}")
                await ctx.send(f"Done, reloaded {cog}")
            except Exception as e:
                await ctx.send(e)


    @commands.command(name="unload", aliases=["u"])
    async def unload(self, ctx: commands.Context, cog: str):
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
                await ctx.send("Done")
            except Exception as e:
                await ctx.send(e)



    @commands.command(name="load", aliases=["l"])
    async def load(self, ctx: commands.Context, cog: str):
        if cog in {"a", "all"}:
            for ext in list(self.bot.extensions):
                try:
                    self.bot.load_extension(ext)
                    await ctx.send(f"Done")
                except Exception as e:
                    await ctx.send(e)
                    traceback.print_exc()
        else:
            try:
                self.bot.load_extension(f"cogs.{cog}")
                await ctx.send("Done")
            except Exception as e:
                await ctx.send(e)


def setup(bot: RoboAy):
    bot.add_cog(Owner(bot))
