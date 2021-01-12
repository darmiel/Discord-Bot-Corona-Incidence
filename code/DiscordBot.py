import nest_asyncio
import discord
import WebScraping
import os
from dotenv import load_dotenv
from importlib import reload
from datetime import date


load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

dictionary = WebScraping.dictgenerator()

client = discord.Client()

@client.event
async def on_ready():
    print("Bot started and connected to Discord...")

@client.event
async def on_message(message):
    try:
        command = message.content
        reload(WebScraping)
        if command.startswith("😷"):          
            countie = message.content
            printcommand = WebScraping.findCountie(countie,dictionary)
            await message.channel.send(printcommand)
            return
        elif command == "!update":
            await message.channel.send("Updating Data...")
            response = WebScraping.downloadData()
            await message.channel.send(response)
            return
    except Exception as e:
        print("Error occured: " + e)

client.run(TOKEN)

