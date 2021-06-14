from __future__ import annotations

import logging
import traceback
import os
from datetime import datetime as dt

import aiohttp
import discord
from discord.ext import commands
import mystbin
import creds

def get_prefix(bot, msg):
    return commands.when_mentioned_or(bot.prefixes)

initial_extensions = (
    "jishaku",
    "cogs.buttons",
    "cogs.owner"
)

log = logging.getLogger("discord")
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
log.addHandler(handler)


class RoboAy(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = get_prefix,
                        description = "A bot made to test some things",
                        case_insensitive = True,
                        intents = discord.Intents.all(),
                        allowed_mentions = discord.AllowedMentions.none(),
                        help_command = commands.MinimalHelpCommand(),
                        status = discord.Status.online,
                        activity = discord.Activity(type=discord.ActivityType.playing, name="ra help"),
                        owner_ids = {681183140357865474, 803147022374535189}
                        )
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()
        self.session = aiohttp.ClientSession()
        self.mystbin = mystbin.Client(session=self.session)
        self.prefixes = ["owo ", "ra ", "Ra "]


    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = dt.utcnow()
        log.info("Logged in")
        print(f"Logged in as {self.user}\nID: {self.user.id}")
        print(f"Discord Version: {discord.__version__}")


    # async def get_context(self, message, *, cls=None):
    #     return await super().get_context(cls=cls or commands.Context)


    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, (commands.CheckFailure, commands.NotOwner, commands.CommandNotFound)):
            return
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(str(error))
        await ctx.send(str(await self.mystbin.post(traceback.format_exc(), syntax="python")))


    async def process_commands(self, msg: discord.Message):
        ctx = await self.get_context(msg)
        try:
            await self.invoke(ctx)
        except Exception:
            raise


    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.content in (
            f"<@{self.user.id}>",
            f"<@!{self.user.id}>"
        ):
            await msg.channel.send("My prefix is `ra `")
        await self.process_commands(msg)


    os.environ['JISHAKU_NO_UNDERSCORE'] = 'True'
    os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'
    os.environ['JISHAKU_HIDE'] = 'True'
    os.environ['NO_COLOR'] = 'True'


    def run(self, *args, **kwargs):
        for ext in initial_extensions:
            try:
                self.load_extension(ext)
                log.info(f"{ext} has loaded.")
            except Exception as e:
                log.critical(f"'{ext}' did not load. Traceback: {e}")
                traceback.print_exc()
        super().run(creds.standle_token, reconnect=True, *args, **kwargs)


if __name__ == "__main__":
    bot = RoboAy()
    bot.run()
