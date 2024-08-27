import discord
import json

intents = discord.Intents.all()

def load_server_settings():
    try:
        with open('server_settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error reading server_settings.json. File may be corrupted.")
        return {}

def save_server_settings(settings):
    with open('server_settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

def get_prefix(bot, message):
    settings = load_server_settings()
    return settings.get(str(message.guild.id), {}).get('prefix', '?')

def load_jokes():
    try:
        with open('jokes.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("jokes.txt file not found.")
        return []

jokes = load_jokes()

def update_user_status(guild_id, user_id, username, status, reason=None):
    settings = load_server_settings()
    if str(guild_id) not in settings:
        settings[str(guild_id)] = {}
    if 'user_statuses' not in settings[str(guild_id)]:
        settings[str(guild_id)]['user_statuses'] = {}
    settings[str(guild_id)]['user_statuses'][str(user_id)] = {
        'username': username,
        'status': status,
        'reason': reason,
        'user_id': str(user_id)  # Add this line to store the user ID
    }
    save_server_settings(settings)

def remove_user_status(guild_id, user_id):
    settings = load_server_settings()
    if str(guild_id) in settings and 'user_statuses' in settings[str(guild_id)]:
        if str(user_id) in settings[str(guild_id)]['user_statuses']:
            del settings[str(guild_id)]['user_statuses'][str(user_id)]
            save_server_settings(settings)

def get_user_status(guild_id, user_id):
    settings = load_server_settings()
    if str(guild_id) in settings and 'user_statuses' in settings[str(guild_id)]:
        return settings[str(guild_id)]['user_statuses'].get(str(user_id))
    return None