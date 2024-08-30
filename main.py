import discord
import os
import requests
from discord.ext import commands
from keep_alive import keep_alive

# Your API key for the jokes service
headers = {"Accept": "application/json"}

# Create an instance of a Bot. This bot represents your bot.
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Use the existing command tree from the bot instance
tree = bot.tree

# Event listener for when the bot has connected to Discord


@bot.event
async def on_ready():
    await tree.sync()  # Sync the slash commands with Discord
    print(f'We have logged in as {bot.user}')

# Define a slash command


@tree.command(name="ping", description="Responds with 'yo what the zii...'")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('yo what the zii...')


@tree.command(name="joke", description="Tells a random joke")
async def joke(interaction: discord.Interaction):
    try:
        response = requests.get("https://icanhazdadjoke.com/", headers=headers)
        response.raise_for_status()  # Check if the request was successful
        joke = response.json()["joke"]
        await interaction.response.send_message(joke)
    except requests.RequestException as e:
        await interaction.response.send_message('Error fetching joke.')


@tree.command(name="delete", description="Deletes a specified number of messages")
async def delete(interaction: discord.Interaction, number: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("You do not have permission to delete messages.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)  # Acknowledge the interaction
    deleted = await interaction.channel.purge(limit=number)
    await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)


keep_alive()
# Run the bot with the token
bot.run(os.environ['TOKEN'])
