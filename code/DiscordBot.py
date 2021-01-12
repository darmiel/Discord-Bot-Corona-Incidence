# -*- coding: utf-8 -*-
#%%
import nest_asyncio
import discord
import WebScraping

with open(r"E:\VSC\Inzidenz\token.txt") as myfile:
    token = [next(myfile) for x in range(1)]

dictionary = WebScraping.dictgenerator()

client = discord.Client()
@client.event
async def on_message(message):
        if message.content.startswith("!"):
          
            countie = message.content
            printcommand = WebScraping.findCountie(countie,dictionary)
            await message.channel.send(printcommand)
            return
       
nest_asyncio.apply()            
client.run(token[0])
# %%
