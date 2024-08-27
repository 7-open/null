import discord
from discord.ext import commands
import asyncio

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_task = None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def usercount(self, ctx):
        """Create or update user count channels."""
        guild = ctx.guild

        async def create_or_update_channel(name, count):
            existing_channel = discord.utils.get(guild.voice_channels, name=name.split(":")[0])
            if existing_channel:
                await existing_channel.edit(name=f"{name}: {count}")
            else:
                await guild.create_voice_channel(name=f"{name}: {count}", category=None)

        async def update_counts():
            while True:
                await asyncio.sleep(300)  # Wait for 5 minutes
                total_users = len(guild.members)
                human_users = len([m for m in guild.members if not m.bot])
                bot_users = len([m for m in guild.members if m.bot])
                await create_or_update_channel("👥 Total Users", total_users)
                await create_or_update_channel("👤 Human Users", human_users)
                await create_or_update_channel("🤖 Bot Users", bot_users)

        total_users = len(guild.members)
        human_users = len([m for m in guild.members if not m.bot])
        bot_users = len([m for m in guild.members if m.bot])

        await create_or_update_channel("👥 Total Users", total_users)
        await create_or_update_channel("👤 Human Users", human_users)
        await create_or_update_channel("🤖 Bot Users", bot_users)

        await ctx.send("User count channels have been created/updated!")

        if self.update_task:
            self.update_task.cancel()
        self.update_task = self.bot.loop.create_task(update_counts())

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nousercount(self, ctx):
        """Remove user count channels and stop updates."""
        guild = ctx.guild
        if self.update_task:
            self.update_task.cancel()
            self.update_task = None

        channels_to_remove = ["👥 Total Users", "👤 Human Users", "🤖 Bot Users"]
        for channel_name in channels_to_remove:
            channel = discord.utils.get(guild.voice_channels, name=channel_name.split(":")[0])
            if channel:
                await channel.delete()

        await ctx.send("User count channels have been removed and updates stopped.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def req(self, ctx):
        """Create all required roles for the bot's functionality.
        Usage: ?req
        """
        required_roles = [
            ("Muted", discord.Color.light_grey()),
            ("DJ", discord.Color.blue()),
            ("Moderator", discord.Color.green()),
            ("Admin", discord.Color.red())
        ]

        created_roles = []
        existing_roles = []

        for role_name, role_color in required_roles:
            existing_role = discord.utils.get(ctx.guild.roles, name=role_name)
            if existing_role:
                existing_roles.append(role_name)
            else:
                new_role = await ctx.guild.create_role(name=role_name, color=role_color)
                created_roles.append(role_name)

        response = "Required roles setup complete.\n"
        if created_roles:
            response += f"Created roles: {', '.join(created_roles)}\n"
        if existing_roles:
            response += f"Already existing roles: {', '.join(existing_roles)}"

        await ctx.send(response)
        
async def setup(bot):
    await bot.add_cog(AdminCog(bot))