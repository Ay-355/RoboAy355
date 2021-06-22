from __future__ import annotations
import asyncio

from typing import TYPE_CHECKING
import traceback
import os
import importlib

import discord
from discord.ext import commands
from utils.context import RContext

if TYPE_CHECKING:
    from bot import RoboAy



class Owner(commands.Cog):
    def __init__(self, bot: RoboAy) -> None:
        self.bot = bot

    def cog_check(self, ctx: RContext) -> bool:
        if ctx.author.id in self.bot.owner_ids:
            return True
        raise commands.NotOwner()


    @commands.command(name="reload", aliases=["r"])
    async def reload(self, ctx: RContext, cog: str):
        """Reloads an extension, or all of them"""
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
            await ctx.done()
        except Exception as e:
            await ctx.send(e)


    @commands.command(name="unload", aliases=["u"])
    async def unload(self, ctx: RContext, cog: str):
        """Unloads an extension, or all of them"""
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
        """Loads an extension or all of them"""
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



    @commands.command(name="nopresence", aliases=["np"])
    async def no_presence(self, ctx: RContext):
        """Resets the activity. Useful for when hosting 2 instances of a bot"""
        await self.bot.change_presence(activity=None)
        await ctx.done()


    @commands.command(name="dm")
    async def _dm(self, ctx: RContext, user: discord.User, *, message: str):
        """Dm's a user"""
        try:
            await user.send(message)
        except:
            await ctx.send("Failed to send message (DM's closed?).")


    @commands.command(name="utils")
    async def _utils(self, ctx: RContext, module: str):
        """Reloads a utils module"""
        utilsEmbed = discord.Embed(title="Utils Reload")
        if module in {"a", "all"}:
            for f in os.listdir("./utils"):
                if f.endswith(".py"):
                    try:
                        _module = importlib.import_module(f"utils.{f[:-3]}")
                        importlib.reload(_module)
                        utilsEmbed.add_field(name=f"Reloaded", value=f)
                    except:
                        utilsEmbed.add_field(name=f"Error", value=traceback.format_exc())
            return await ctx.send(embed=utilsEmbed)
        try:
            _module = importlib.import_module(f"utils.{module}")
            importlib.reload(_module)
        except ModuleNotFoundError:
            return await ctx.send(f"No module named {module}")
        except:
            return await ctx.send(f"Error occurred -> {traceback.format_exc()}")
        await ctx.done()


    @commands.command(name="clean")
    async def clean(self, ctx: RContext, number: int = None):
        """Cleans up the bot's messages"""
        def check(m: discord.Message):
            return m.author == self.bot.user

        if number is None:
            return (await ctx.ref_res.delete() if ctx.ref else await ctx.send('No Message to delete'))
        n = await ctx.channel.purge(limit=number, check=check)
        await ctx.send(f"Purged {len(n)} messages")


    @commands.group(name="edit", aliases=["change", "set"])
    async def edit(self, ctx: RContext):
        if ctx.invoked_subcommand is None:
            return await ctx.send("Send an action.")


    @edit.command(name="name")
    async def edit_username(self, ctx: RContext, *, username: str):
        """Change the bot's username"""
        try:
            await self.bot.user.edit(username=username)
            await ctx.send(embed=discord.Embed(title="Success", description=f"Changed my username to `{username}`"))
        except Exception as e:
            await ctx.send(e)



    @edit.command(name="avatar")
    async def edit_avatar(self, ctx: RContext, image = None):
        """Change the bot's avatar"""
        url = None
        if a := ctx.message.attachments:
            url = a[0].proxy_url
        else: 
            url = image  #too lazy for anything else, never gonna actually change it anyways
        async with ctx.session.get(url) as res:
            if res.status == 200:
                await self.bot.user.edit(avatar=await res.read())
                await ctx.done()
            else:
                return await ctx.send("Could not change avatar, image was probably not a link")


    @edit.command(name="nick")
    async def edit_nick(self, ctx: RContext, *, nick: str):
        """Changes the bot's nickname in the current guild"""
        await ctx.guild.me.edit(nick=nick)
        await ctx.send(f"My nickname is now {nick}")


    @commands.command(name="leaveguild")
    async def leave_guild(self, ctx: RContext, guild: discord.Guild = None):
        """Leaves a guild. Should never be used"""
        guild = guild or ctx.guild
        await ctx.send(f"Are you sure you want to leave this guild? -> {guild.name} ({guild.id})")
        try:
            m = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=25.0)
        except asyncio.TimeoutError:
            return await ctx.send("Ok cancelling")
        else:
            if m.content not in {"yes", "true", "yeah"}:
                return await ctx.send("Cancelling...")
            await guild.leave()
            await ctx.done()


def setup(bot: RoboAy):
    bot.add_cog(Owner(bot))
