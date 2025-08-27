import discord
import json
import time
import datetime
import sys

import csv_parser as PARSER

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_task_list():
    output = ""
    for i in range(int(len(todo_list))):
        output = output + f"{i+1}. " + todo_list[i] + '\n'
    return output

@client.event
async def on_ready():
    message_string = ""
    x = datetime.datetime.now()
    message_string = message_string + x.strftime("%A, %B %d") + '\n' # day
    message_string = message_string + get_task_list() # list of tasks

    channel = client.get_channel(1258561761024675860)
    msg = await channel.send(message_string)
    emoji_list = ["\U0001F525"]
    for emoji in emoji_list:
        await msg.add_reaction(emoji)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    command_list = message.content.lower().split(' ')
    match command_list[0]:
        case "!list":
            await message.channel.send(get_task_list())
        case "!complete":
            try:
                todo_list.pop(int(command_list[1])-1)
            except:
                await message.channel.send("Invalid task input")
        case "!ledger":
            if len(command_list) == 1:
                await message.channel.send("Add 'form' 'sheet', or 'tally'.")
            else:
                if command_list[1] == "form":
                    await message.channel.send("https://docs.google.com/forms/d/e/1FAIpQLSfaBtMKh4bCJMJZmReW2cJXCuZs5F8ykFopeiyBRrC5EEKfCw/viewform?usp=sharing&ouid=118416168224866076667")
                elif command_list[1] == "sheet":
                    await message.channel.send("https://docs.google.com/spreadsheets/d/1i34QFwZm6M4C4QK3T2ftL7evNOpUBQH1KNSHYEA54tM/edit?usp=sharing")
                elif command_list[1] == "tally":
                    tally_string = PARSER.tally_transactions()
                    print(tally_string)
                    await message.channel.send(tally_string)

                
# init process
f = open("C:\\Tree's Stuff\\discord_tokens\\calendar.json", "r")
token = json.loads(f.read()).get("token")

# loading in the data for the to-do list
list_file = open("./list.json", "r")
list_dict = json.loads(list_file.read())
todo_list = list(list_dict.values())
print(todo_list)

client.run(token)