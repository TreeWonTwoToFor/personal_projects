import random
import discord
import os
import json
import math
import datetime

from data import join_list

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

command_dict = {
    "help": "Use this command to look up how to use specific commands. Use !list to show all commands",
    "list": "Shows all of the possible commands",
    "snipe": "This is how you snipe other people. Just call the command with their username, and you get a snipe on them!",
    "leaderboard": "Use this command to see who has the most snipes, or who is sniped the most."
}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    command_list = message.content.lower().split(' ')
    match command_list[0]:
        case "!help":
            if len(command_list) == 1:
                await message.channel.send(command_dict["help"])
            else:
                try:
                    await message.channel.send(command_dict[command_list[1]])
                except:
                    await message.channel.send("Please make sure to enter a valid command")
        case "!list":
            await message.channel.send(command_dict.keys())
        case "!snipe":
            file = open("log.txt", "r")
            old_text = file.read()
            file = open("log.txt", "w")
            now = datetime.datetime.now()
            formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
            name = message.author.nick
            if name == None:
                name = message.author
            new_text = old_text + (f"{formatted_date}: {name} -> {command_list[1]}\n")
            file.write(new_text)
            await message.channel.send(f"{name} sniped {command_list[1]}!")
        case "!leaderboard" | "!lb":
            file_text = open('log.txt', 'r').read()
            words = file_text.split()
            person_list = []
            for i in range(0, len(words), 5):
                if len(person_list) == 0:
                    person_list.append([words[i+2], 1])
                else:
                    found = False
                    for person in person_list:
                        if person[0] == words[i+2]:
                            person[1] += 1
                            found = True
                    if not found:
                        person_list.append([words[i+2], 1])
            person_list.sort(key=lambda x: x[1])
            person_list.reverse()
            output = "```"
            for i in range(0, len(person_list)):
                person = person_list[i]
                if i < 10:
                    output = output + str(i+1) + ": " + person[0] + " - " + str(person[1]) + "\n"
            output = output + "```"
            await message.channel.send(output)
        

os.system("cls")
f = open("C:\\JSGames\\discord_tokens\\sniper.json", "r")
# f = open("C:\\Tree's Stuff\\discord_tokens\\banshee.json", "r")
client.run(json.loads(f.read()).get("token"))
