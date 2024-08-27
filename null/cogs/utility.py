import discord
from discord.ext import commands
from utils import get_prefix, load_server_settings, save_server_settings

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx, command_name=None):
        """Display help information for commands."""
        prefix = get_prefix(self.bot, ctx.message)

        if command_name:
            command = self.bot.get_command(command_name)
            if command:
                embed = discord.Embed(title=f"Help: {prefix}{command.name}", color=discord.Color.blue())
                embed.add_field(name="Description", value=command.help or "No description available.", inline=False)
                embed.add_field(name="Usage", value=f"{prefix}{command.name} {command.signature}", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Command '{command_name}' not found.")
            return

        embed = discord.Embed(title="Bot Commands", description="Here are the commands you can use:", color=0x00ff00)
        for cog_name, cog in self.bot.cogs.items():
            commands_list = []
            for command in cog.get_commands():
                if command.hidden:
                    continue
                if command.checks:
                    try:
                        if not await discord.utils.async_all(check(ctx) for check in command.checks):
                            continue
                    except:
                        continue
                commands_list.append(f"`{prefix}{command.name}`: {command.help.split('.')[0] if command.help else 'No description'}")
            if commands_list:
                embed.add_field(name=cog_name, value="\n".join(commands_list), inline=False)

        embed.set_footer(text=f"Use '{prefix}help <command>' for more info on a command.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix: str):
        """Change the command prefix for the server."""
        if len(new_prefix) > 3:
            await ctx.send("Prefix must be 3 characters or less.")
            return

        settings = load_server_settings()
        if str(ctx.guild.id) not in settings:
            settings[str(ctx.guild.id)] = {}
        settings[str(ctx.guild.id)]['prefix'] = new_prefix
        save_server_settings(settings)

        await ctx.send(f"Prefix has been set to: {new_prefix}")
        await self.bot.change_presence(activity=discord.Game(name=f"{new_prefix}help for commands"))

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Get information about a user."""
        member = member or ctx.author
        roles = [role.mention for role in member.roles[1:]]

        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Guild name:", value=member.display_name)
        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(roles) or "None")
        embed.add_field(name="Top role:", value=member.top_role.mention)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))