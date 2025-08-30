import discord
import json
import time
import datetime
import sys

import csv_parser as PARSER

# setup for discord side
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# links for google sheets and forms
google_sheet = open(
    "/home/jonathan/discord_calendar_links/google_sheets.txt", 'r').read()
google_form = open(
    "/home/jonathan/discord_calendar_links/google_form.txt", 'r').read()

# todo list functions
def get_task_list():
    output = ""
    if len(todo_list) == 0:
        return "There's nothing on the To-Do list."
    for i in range(int(len(todo_list))):
        output = output + f"{i+1}. " + todo_list[i] + '\n'
    return output

def update_todo_list(todo_list):
    list_dict = {}
    for i in range(len(todo_list)):
        list_dict[i+1] = todo_list[i]
    with open("./list.json", "w") as json_file:
        json.dump(list_dict, json_file, indent=2)

# discord specific functions
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
        case "!help":
            await message.channel.send("Use !list or !ledger to get started.")
        case "!list":
            if len(command_list) == 1:
                await message.channel.send("Add 'show' 'add', or 'complete'.")
            elif command_list[1] == "show":
                await message.channel.send(get_task_list())
            elif command_list[1] == "add":
                if len(command_list) > 2:
                    task_input = ""
                    for word in (command_list[2:]):
                        task_input = task_input + " " + word
                    todo_list.append(task_input)
                    update_todo_list(todo_list)
                    await message.channel.send(
                        f"Task '{task_input.strip()}' has been added.")
                else:
                    await message.channel.send(
                        "Invalid task input")
            elif command_list[1] == "complete":
                task_complete = False
                try:
                    todo_list.pop(int(command_list[2])-1)
                    task_complete = True
                except:
                    await message.channel.send(
                        "Invalid task input")
                if task_complete:
                    try:
                        update_todo_list(todo_list)
                        await message.channel.send(
                            "Completed Task.")
                    except:
                        await message.channel.send(
                            "File couldn't be updated")
        case "!ledger":
            if len(command_list) == 1:
                await message.channel.send("Add 'form' 'sheet', or 'tally'.")
            else:
                if command_list[1] == "form":
                    # link to the google form
                    await message.channel.send(google_form)
                elif command_list[1] == "sheet":
                    #link to the google sheet
                    await message.channel.send(google_sheet)
                elif command_list[1] == "tally":
                    tally_string = PARSER.tally_transactions()
                    print(tally_string)
                    await message.channel.send(tally_string)

                
# init process
#f = open("C:\\Tree's Stuff\\discord_tokens\\calendar.json", "r") # WINDOWS
f = open("/home/jonathan/token/calendar.json", "r") # LINUX
token = json.loads(f.read()).get("token")

# loading in the data for the to-do list
list_file = open("./list.json", "r")
list_dict = json.loads(list_file.read())
todo_list = list(list_dict.values())
print(todo_list)

client.run(token)
