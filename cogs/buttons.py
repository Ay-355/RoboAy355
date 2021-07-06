from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord
from discord import ui
from discord.ext import commands
from utils.context import RContext

if TYPE_CHECKING:
    from bot import RoboAy

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        # sourcery skip: hoist-statement-from-if
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                assert isinstance(child, discord.ui.Button) # just to shut up the linter
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):  # sourcery skip: switch
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class CompetitionView(ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.pressed = {}
        self.m = "Competition\n--------------\n"


class CompetitionButton(ui.Button["CompetitionView"]):
    def __init__(self):
        super().__init__(label="How many times can you click this?", style=discord.ButtonStyle.blurple)

    async def callback(self, interaction: discord.Interaction):
        try:
            self.view.pressed[interaction.user.id] += 1
        except KeyError:
            self.view.pressed[interaction.user.id] = 1
        msg = "{p} has pressed **{n}** times\n"
        final = "".join(
            msg.format(
                p=self.view.ctx.guild.get_member(person).name,
                n=self.view.pressed[person],
            )
            for person in self.view.pressed.keys()
        )

        await interaction.response.edit_message(content=self.view.m + final)


class TotalView(ui.View):
    def __init__(self):
        super().__init__()
        self.m = "People who have clicked the button\n----------------------------"


class TotalButton(ui.Button["TotalView"]):
    def __init__(self):
        super().__init__(label="Click This", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        self.view.m += f"\n{interaction.user.name}"
        await interaction.response.edit_message(content=self.view.m)



# class WhackAMoleView(ui.View):
#     ...


# class WhackAMoleButton(ui.Button):
#     ...


class RPSView(ui.View):
    def __init__(self):
        super().__init__()


class RPSButton(ui.Button["RPSView"]):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.secondary)
    
    async def callback(self, interaction: discord.Interaction):
        ...


class Buttons(commands.Cog):
    def __init__(self, bot: RoboAy) -> None:
        self.bot = bot


    @commands.command("plsdontspamthis", aliases=["pdst"])
    async def plsdontpsamthis(self, ctx: RContext):
        """Sends a button that adds you name to the message"""
        v = TotalView()
        v.add_item(TotalButton())
        await ctx.send(content="Please don't spam this", view=v)
        await ctx.done()
        await v.wait()


    @commands.command(name="ttt")
    async def tic(self, ctx: RContext):
        """The classic tictactoe with buttons"""
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())
        await ctx.done()

    @commands.command(name="comp")
    async def _comp(self, ctx: RContext):
        """Who can press the button the most?"""
        v = CompetitionView(ctx)
        v.add_item(CompetitionButton())
        await ctx.send("Click It", view=v)
        await ctx.done()
        await v.wait()


    # @commands.command(name="rps")
    # async def _rps(self, ctx: RContext):
    #     v = RPSView()
    #     await ctx.send("Rock Paper Scissors", view=v)


def setup(bot: RoboAy):
    bot.add_cog(Buttons(bot))
