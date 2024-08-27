import discord
from discord.ext import commands
import asyncio
import os
from config import DEFAULT_PREFIX
from utils import get_prefix, intents

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

# Load cogs
initial_extensions = [
    'cogs.moderation',
    'cogs.utility',
    'cogs.fun',
    'cogs.admin'
]

async def load_extensions():
    for extension in initial_extensions:
        await bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name=f"{DEFAULT_PREFIX}help for commands"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command.")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check the command usage.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

async def main():
    await load_extensions()
    await bot.start(os.getenv('TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())