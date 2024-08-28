import discord
import os
import requests
from keep_alive import keep_alive

# Your API key for the jokes service
headers = {"Accept": "application/json"}

# Create an instance of a Client. This client represents your bot.
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Event listener for when the bot has connected to Discord
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event listener for when a message is sent in the chat
@client.event
async def on_message(message):
    # Prevent the bot from replying to itself
    if message.author == client.user:
        return

    # Respond to specific messages
    if message.content.startswith('!ping'):
        await message.channel.send('yo what the zii...')

    if message.content.startswith('!joke'):
        try:
            response = requests.get("https://icanhazdadjoke.com/", headers=headers)
            response.raise_for_status()  # Check if the request was successful
            joke = response.json()["joke"]
            await message.channel.send(joke)
        except requests.RequestException as e:
            await message.channel.send('Error fetching joke.')

keep_alive()
# Run the bot with the token
client.run(os.environ['TOKEN'])
