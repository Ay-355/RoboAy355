from __future__ import annotations

from typing import TYPE_CHECKING
import traceback

import discord
from discord.ext import commands
from utils.context import RContext

if TYPE_CHECKING:
    from bot import RoboAy


class Events(commands.Cog):
    def __init__(self, bot: RoboAy) -> None:
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx: RContext, error):
        """Error Handler"""
        if (
            hasattr(ctx.command, "on_error")
            or (ctx.command and hasattr(ctx.cog, f"_{ctx.command.cog_name}__error"))
        ):
            return

        error = getattr(error, "original", error)


        str_errors = ( # eh
            discord.Forbidden,
            commands.BadArgument,
            commands.BadBoolArgument,
            commands.BadColourArgument,
            commands.BadUnionArgument,
            commands.MaxConcurrencyReached,
            commands.TooManyArguments,
            commands.MemberNotFound, 
            commands.GuildNotFound, 
            commands.RoleNotFound, 
            commands.ChannelNotFound, 
            commands.EmojiNotFound, 
            commands.UserNotFound,
            commands.MessageNotFound,
        )

        if isinstance(error, (commands.CommandNotFound, commands.CheckAnyFailure, commands.CheckFailure, commands.NotOwner, commands.DisabledCommand)):
            return

        elif isinstance(error, str_errors):
            return await ctx.send(str(error))

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"Please pass the `{error.param.name}` parameter\nCorrect Usage:  `{ctx.clean_prefix}{ctx.command.name} {ctx.command.signature}`")

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send(f"Command `{ctx.command.name}` can not be used in private messages")


        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(
                f"You need the " 
                + ", ".join(
                    perm.replace("_", " ").replace("guild", "server").title()
                    for perm in error.missing_perms
                ) 
                + " permission(s) to carry out that command!\nTry again when you have them."
            )

        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(
                f"I need the "
                + ", ".join(
                    perm.replace("_", " ").replace("guild", "server").title()
                    for perm in error.missing_perms
                )
                + " permission(s) to carry out that command!"
            )

        else:
            tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__, 1))
            if hasattr(self.bot.creds, "name"):
                tb = tb.replace(self.bot.creds.name, "Ay355") # safety things
            final = str(await self.bot.mystbin.post(tb)) if len(tb) > 1800 else f'```\n{tb}\n```'
            await ctx.send(f"An Unknown Error has occurred: \n{final}")
            raise error


def setup(bot: RoboAy):
    bot.add_cog(Events(bot))
