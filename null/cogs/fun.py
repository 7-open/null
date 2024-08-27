import discord
from discord.ext import commands
import random
from utils import jokes

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Ask the magic 8ball a question."""
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
            "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
            "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."
        ]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @commands.command()
    async def coinflip(self, ctx):
        """Flip a coin."""
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"The coin landed on: {result}")

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Roll dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send("Format has to be in NdN!")
            return
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command()
    async def joke(self, ctx):
        """Tell a random joke."""
        await ctx.send(random.choice(jokes))

    @commands.command()
    async def meme(self, ctx):
        """Show a random meme."""
        memes = [
            "https://i.imgur.com/1oyOPAa.png",
            "https://i.imgur.com/wZw2xXI.png",
            "https://i.imgur.com/lMoOq2N.png",
            "https://i.imgur.com/gF43sJ9.png",
            "https://i.imgur.com/TtMINsZ.png"
        ]
        embed = discord.Embed()
        embed.set_image(url=random.choice(memes))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FunCog(bot))