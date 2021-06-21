from __future__ import annotations

import discord
from discord.ext import commands
import re
from typing import Optional, TYPE_CHECKING, Union
from aiohttp import ClientSession

if TYPE_CHECKING:
    from bot import RoboAy


class RContext(commands.Context):
    
    bot: RoboAy

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    async def done(self):
        """Adds a green check mark to the authors message"""
        return await self.message.add_reaction("<:greenTickAnimated:856318806656548865>")


    @property
    def disp(self) -> discord.Member.display_name:
        """Shortcut to retrieve the authors display name"""
        return self.author.display_name


    @property
    def qualn(self) -> commands.Command.qualified_name:
        """Shortcut to retrieve the commands name"""
        return self.command.qualified_name


    @property
    def ref(self) -> Optional[discord.MessageReference]:
        """Shortcut to retrieve the messages reference"""
        return self.message.reference


    @property
    def ref_res(self) -> Optional[Union[discord.DeletedReferencedMessage, discord.Message]]:
        """Shortcut to retrieve the replied message"""
        return self.message.reference.resolved


    @property
    def attach(self) -> list[discord.Attachment]:
        """Shortcut to retrieve the messages attachments"""
        return self.message.attachments


    @property
    def session(self) -> ClientSession:
        """Shortcut to retrieve the bots session"""
        return self.bot.session


    @property
    def clean_prefix(self) -> str:
        """Returns a ``clean_prefix`` Which changes mention prefixes to the bot's prefix"""
        return re.sub(f"<@!?{self.bot.user.id}>", f"@{self.bot.user.name}", self.prefix)
