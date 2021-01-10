# -*- coding: utf-8 -*-
#%%
import nest_asyncio
from dotenv import dotenv_values
import discord

with open(r"E:\VSC\Inzidenz Landkreise\token.txt") as myfile:
    token = [next(myfile) for x in range(1)]





import WebScraping

dictionary = WebScraping.dictgenerator()

client = discord.Client()
@client.event
async def on_message(message):
        if message.content.startswith("!"):
          
            landkreis = message.content
            printcommand = WebScraping.findLK(landkreis,dictionary)
            await message.channel.send(printcommand)
            return
       
nest_asyncio.apply()            
client.run(token[0])
# %%
