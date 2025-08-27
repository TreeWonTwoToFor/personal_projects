import discord
import json
import time
import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
seconds_in_day = 24*60*60

@client.event
async def on_ready():
    running = True
    while running:
        day = datetime.date.today()
        channel = client.get_channel(1258561761024675860)
        msg = await channel.send(str(day))
        emoji_list = ["\U0001F4AA", "\U0001F6BF", "\U0001F95E", "\U0001F354", "\U0001F4BB", "\U00003297", "\U00002B1C", "\U0001F7E6"]
        for emoji in emoji_list:
            await msg.add_reaction(emoji)
        time.sleep(seconds_in_day)


f = open("calendar.json", "r")
client.run(json.loads(f.read()).get("token"))