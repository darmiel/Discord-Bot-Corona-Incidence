import discord

import scraper

from settings import settings
from keyboard import KeyboardLayout

if __name__ == "__main__":
  # create keyboard layout
  deDE = KeyboardLayout([
    "QWERTZUIOPÜ+",
    "ASDFGHJKLÖÄ#",
    "<YXCVBNM,.-"
  ])

  # create discord client
  client = discord.Client()

  # register events
  PREFIX: str = settings["Prefix"]
  @client.event
  async def on_message(message: discord.Message):
    content: str = message.content
    if not content.startswith(PREFIX):
      return

    # remove prefix
    content = content[len(PREFIX):].strip()
    reply: discord.Message = await message.reply(f"⏱ Suche nach **{content}**...")

    # find nearest
    stats = scraper.get_stats()
    matches, mode = scraper.find_nearest(content, stats, deDE)

    # no match found
    if len (matches) == 0:
      await reply.edit(f"😕 `{content}` nicht gefunden.")
      return
      
    # build embed message
    embed = discord.Embed(title=f"😷 Incidence for **{content}**", description=f"{len(matches)} Übereinstimmungen gefunden | {mode}", color=7505584)

    for m in matches:
      name = m[0]
      val = stats[name]
      cases = round(val["cases"], 2)
      embed.add_field(name=f"👉 {name}", value=f"{cases}", inline=True)

    await reply.edit(content="🤗", embed=embed)
  # login
  client.run(settings["Token"])
