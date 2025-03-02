import random
import discord
import os
import json
import math

from data import variables
from data import ghost_dict
from data import item_dict
from data import Item

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def join_list(list, spacer, is_multiline=False):
    if is_multiline:
        return '```'+spacer.join(map(str, list))+'```'
    else:
        return spacer.join(map(str, list))

def level_lookup(rank):
    lb_list = []
    output_list = []
    width = 5
    if rank == 1:
        width = 9
    if rank > 75:
        rank = 75
    for i in range(0,len(variables.level_dictonary)-1):
        level_list = variables.level_dictonary.get("level_list")
        item_ranks = variables.level_dictonary.get(level_list[i])
        for j in range(0, len(item_ranks)):
            if item_ranks[j] >= rank:
                lb_list.append((level_list[i],item_ranks[j]))
    lb_list.sort(key=lambda x: x[1])
    for k in range(0, width):
        output_list.append(lb_list[k])
    return level_clean(output_list)

def level_clean(unclean_item):
    output_list = []
    for i in range(0, len(unclean_item)):
        output = str(unclean_item[i])
        output = output.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
        output = output.split()
        new_output = output[1] + ": " + output[0]
        output_list.append(new_output)
    return output_list

def help_list(help):
    match help:
        case "help":
            return "Welcome to the help command! It tells you about different commands, use this format to learn more about commands ```!help command```"
        case "list":
            return "The list command lists the different commands that you can use. It also gives a short description."
        case "wave":
            return "I will give you a short wave and a greetings. Nothing of use through :)"
        case "evidence":
            return "Allows you to search up ghosts based on a certain type of evidence. The command wihtout parameters will give you the list of evidences. The format for the comamnd is ```!evidence EVIDENCE```"
        case "to-do":
            return "Gives a short to-do list or to-do list of the developer. Feel free to message for more features in the future if it isn't on the list."
        case "map":
            return "Gives a link to a map page that has more information on all of the maps in the game."
        case "wiki":
            return "Gives a link to the Phasmophobia fan wiki."
        case "version":
            return "Gives the version number of the bot. This is used to track which code is being ran."
        case "level":
            return """Returns the level needed to get a specific tier for an item. The format is ```!level flashlight```You can also use this command to list the item options ```!level item```You can also list the items based on your level ```!level list 25```"""
        case "ghost":
            return """Gives a basic description of the ghost you want to learn about. The format is  ```!ghost Banshee```"""
        case "xp":
            return """Tells you how much XP it takes to reach a specific level. If you enter one number, it will give the total amount. If you enter two numbers (current, goal) it will give the amount you need to earn to gain that level."""

def random_game_mode():
    map_index = random.randint(0, 26)
    if map_index <= 17:
        map_index = map_index//3
    elif map_index > 17 and map_index < 23:
        match map_index:
            case 18 | 19: map_index = 6
            case 20 | 21: map_index = 7
            case 22 | 23: map_index = 8
    else:
        map_index = map_index - 15
    map = variables.map_list[map_index]
    difficulty_list = ["Professional", "Nightmare", "3 Evidence Insanity", "Challenge"] 
    difficulty_index = random.randint(0, 5)
    if difficulty_index == 0 or difficulty_index == 1:
        difficulty_index = 0
    elif difficulty_index == 2 or difficulty_index == 3:
        difficulty_index = 1
    else:
        difficulty_index = difficulty_index - 2
    difficulty = difficulty_list[difficulty_index]
    return f"{difficulty} at {map}"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    command_list = message.content.lower().split(' ')
    match command_list[0]:
        case "!wiki":
            await message.channel.send("https://phasmophobia.fandom.com/wiki/Main_Page" )
        case "!version":
            await message.channel.send(variables.version)
        case "!list":
            await message.channel.send(join_list(variables.list_list, "\n", True))
        case "!wave":
            await message.channel.send(":wave: Hello, I'm Banshee Bot! You can start using this bot with the commands !list or !help")
        case "!to-do" | "!todo":
            await message.channel.send(join_list(variables.to_do_list, "\n"))
        case "!random":
            await message.channel.send(random_game_mode())
        case "!help":
            if len(command_list) == 1:
                await message.channel.send(join_list(variables.list_list, "\n", True))
            else:
                try:
                    await message.channel.send(help_list(command_list[1]))
                except:
                    await message.channel.send(help_list("Please make sure to enter a valid command"))
        case "!xp":
            match len(command_list):
                case 1:
                    await message.channel.send("Please enter which level you wish to reach.")
                case 2:
                    level = int(command_list[1])
                    xp = int(100*(level-1)**1.73)
                    await message.channel.send(f"Total XP to reach level {level} is {xp}xp")
                case 3:
                    level_start = int(command_list[1])
                    level_end = int(command_list[2])
                    xp = int(math.fabs(100*(level_end-1)**1.73 - 100*(level_start-1)**1.73))
                    await message.channel.send(f"XP needed to reach level {level_end} from level {level_start} is {xp}xp")
        case "!ghost":
            try:
                if command_list[1] == "list":
                    await message.channel.send(join_list(variables.ghost_list, ", "))
                else:
                    if command_list[1] == "the":
                        ghost = ghost_dict[(command_list[1]).capitalize()+' '+ (command_list[2]).capitalize()]
                    else:
                        if command_list[1] == "mimic" or command_list[1] == "twins":
                            ghost = ghost_dict['The '+ (command_list[1]).capitalize()]
                        else:
                            ghost = ghost_dict[(command_list[1]).capitalize()]
                    await message.channel.send(ghost.simple_output())
            except:
                await message.channel.send("Please make sure you inputted the correct ghost name, or sub-commmand.")
        case "!item":
            try:
                if len(command_list) == 1 or command_list[1] == "list":
                    output = join_list(item_dict["list"], ", ")
                else:
                    tier = 1
                    if command_list[-1].isdigit():
                        tier = int(command_list[-1])
                        command_list.pop()
                    if tier > 3:
                        raise ValueError('User inputted too high of a tier.')
                    item_name = join_list(command_list[1:], '-')
                    item = item_dict[item_name]
                    if type(item) == Item:
                        output = item.simple_output()
                    elif type(item) == list:
                        output = item[tier-1].simple_output()
                await message.channel.send(output)
            except:
                await message.channel.send("Please enter a valid item name/tier")
        case "!level":
            output = ""
            if len(command_list) == 1:
                # !level
                output = "Please enter the name of the item, or your current level. Check !help for details."
            elif len(command_list) > 1:
                try:
                    rank = int(command_list[1])
                    output = join_list(level_lookup(rank), "\n")
                except:
                    if command_list[1] == "item":
                        # !level item
                        output = join_list(variables.level_dictonary.get("level_list"), ", ")
                    else:
                        # !level flashlight
                        item = command_list[1]
                        output = join_list(variables.level_dictonary.get(command_list[1]), ", ")
            await message.channel.send(output)
        case "!evidence":
            if len(command_list) == 1:
                await message.channel.send(join_list(variables.evidence_list, "\n", True))
            else:
                ghost_keys = ghost_dict.keys()
                ghost_list = []
                output_list = []
                evidence = ""
                for ghost_key in ghost_keys:
                    ghost_list.append(ghost_dict[ghost_key])
                match command_list[1]:
                    case "emf":
                        evidence = "EMF"
                        for ghost in ghost_list:
                            if "EMF" in ghost.evidence_list:
                                output_list.append(ghost.name)
                    case "uv" | "ultraviolet":
                        evidence = "UV"
                        for ghost in ghost_list:
                            if "UV" in ghost.evidence_list:
                                output_list.append(ghost.name)
                    case "dots" | "dot":
                        evidence = "DOTs"
                        for ghost in ghost_list:
                            if "DOTs" in ghost.evidence_list:
                                output_list.append(ghost.name)
                    case "freezing" | "temp" | "temperature" | "tempreatures":
                        evidence = "Freezing"
                        for ghost in ghost_list:
                            if "Freezing" in ghost.evidence_list:
                                output_list.append(ghost.name)
                    case "spirit" | "box":
                        evidence = "Spirit Box"
                        for ghost in ghost_list:
                            if "Spirit Box" in ghost.evidence_list:
                                output_list.append(ghost.name)
                    case "orbs" | "gorbs":
                        evidence = "Ghost Orbs"
                        for ghost in ghost_list:
                            if "Ghost Orbs" in ghost.evidence_list:
                                output_list.append(ghost.name)
                    case "writing" | "book":
                        evidence = "Ghost Writing"
                        for ghost in ghost_list:
                            if "Writing" in ghost.evidence_list:
                                output_list.append(ghost.name)
                    case "ghost":
                        if "writing" in command_list:
                            evidence = "Ghost Writing"
                            for ghost in ghost_list:
                                if "Writing" in ghost.evidence_list:
                                    output_list.append(ghost.name)
                        if "orbs" in command_list or "gorbs" in command_list:
                            evidence = "Ghost Orbs"
                            for ghost in ghost_list:
                                if "Ghost Orbs" in ghost.evidence_list:
                                    output_list.append(ghost.name)
                output_list.sort()
                await message.channel.send(f"""Ghosts with {evidence}:```\n""" + join_list(output_list, '\n') + '```')
        case "!map":
            if len(command_list) == 1:
                await message.channel.send('''This website has interactive maps. If you want a specific one, add the map name to the command: https://phasmo.karotte.org/''')
            else:
                if command_list[1] == "list":
                    await message.channel.send(join_list(variables.map_list, ", "))
                elif "ridgeview" in command_list or "court" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/10-ridgeview-court/')
                elif "willow" in command_list or "street" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/13-willow-street/')
                elif "edgefield" in command_list or "road" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/42-edgefield-road/')
                elif "tanglewood" in command_list or "drive" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/6-tanglewood-drive/')
                elif "brownstone" in command_list or "school" in command_list or "high" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/brownstone-high-school/')
                elif "camp" in command_list or "woodwind" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/camp-woodwind/')
                elif "maple" in command_list or "lodge" in command_list or "campsite" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/maple-lodge-campsite/')
                elif "point" in command_list or "hope" in command_list or "lighthouse" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/point-hope/')
                elif "prison" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/prison/')
                elif "sunny" in command_list or "meadows" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/sunny-meadows-mental-institution/')
                elif "bleasedale" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/bleasdale-farmhouse/')
                elif "grafton" in command_list:
                    await message.channel.send('https://phasmo.karotte.org/maps/grafton-farmhouse/')
                elif "farmhouse" in command_list:
                    if "bleasedale" in command_list:
                        await message.channel.send('https://phasmo.karotte.org/maps/bleasdale-farmhouse/')
                    elif "grafton" in command_list:
                        await message.channel.send('https://phasmo.karotte.org/maps/grafton-farmhouse/')
                    else:
                        await message.channel.send("I'm unsure which farmhouse you are talking about. Use 'farmhouse bleasedale', or 'farmhouse grafton'.")
                else:
                    await message.channel.send("I'm unsure which house you are talking about. Use '!map list' if you want the names of the maps.")

os.system("cls")
# f = open("C:\\JSGames\\discord_tokens\\banshee.json", "r")
f = open("C:\\Tree's Stuff\\discord_tokens\\banshee.json", "r")
client.run(json.loads(f.read()).get("token"))
