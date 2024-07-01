import discord
import json
import time
import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

seconds_in_a_day = 24 * 60 * 60

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(".start"):
        running = True
        while running:
            day = datetime.date.today()
            msg = await message.channel.send(str(day))
            emoji_list = ['🏋️‍♂️', '🚿', '🥞', '🍔', '💻', '㊗️', '⬜', '🟦']
            for emoji in emoji_list:
                await msg.add_reaction(emoji)
            time.sleep(2.0)

f = open("C:\\Tree's Stuff\\discord_tokens\\calendar.json", "r")
client.run(json.loads(f.read()).get("token"))