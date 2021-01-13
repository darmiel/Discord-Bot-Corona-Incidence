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
            msg = await message.channel.send("⏰ Searching for county...")
            printcommand = WebScraping.findCountie(countie,dictionary)
            await msg.edit(content=printcommand)
            return
        elif command == "!update":
            msg = await message.channel.send("⏰ Updating Data...")
            response = WebScraping.downloadData()
            if response[0] == True:
                await msg.edit(content=f"✅ Updating Data... Done: {response[1]}")
            else:
                await msg.edit(content=f"❌ Updating Data... Failed: {response[1]}")
            return
    except Exception as e:
        print("Error occured: " + e)

client.run(TOKEN)
