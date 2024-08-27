import discord
from discord.ext import commands
from utils import load_server_settings, save_server_settings
from utils import update_user_status, remove_user_status

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f"{member.name} has been kicked. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member from the server."""
        await member.ban(reason=reason)
        update_user_status(ctx.guild.id, member.id, str(member), 'banned', reason)
        await ctx.send(f"{member.name} has been banned. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Unban a member from the server."""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                remove_user_status(ctx.guild.id, user.id)
                await ctx.send(f"{user.mention} has been unbanned.")
                return

        await ctx.send(f"Could not find {member} in the ban list.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Clear a specified number of messages from the channel."""
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Cleared {amount} messages.", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        """Set the slowmode delay for the current channel."""
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Slowmode set to {seconds} seconds.")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Mute a member in the server."""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)

        await member.add_roles(muted_role, reason=reason)
        update_user_status(ctx.guild.id, member.id, str(member), 'muted', reason)
        await ctx.send(f"{member.mention} has been muted. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban_pull(self, ctx):
        """Get a list of all banned users with their user ID and reason."""
        settings = load_server_settings()
        guild_settings = settings.get(str(ctx.guild.id), {})
        user_statuses = guild_settings.get('user_statuses', {})
        banned_users = [user for user in user_statuses.values() if user['status'] == 'banned']

        if not banned_users:
            await ctx.send("There are no banned users in this server.")
            return

        embed = discord.Embed(title="Banned Users", color=discord.Color.red())
        for user in banned_users:
            embed.add_field(
                name=f"{user['username']}",
                value=f"ID: {user.get('user_id', 'Unknown')}\nReason: {user.get('reason', 'No reason provided')}",
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))