import discord
import os
import json

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# take the evidence needed
# take the ghost dict's truth value for that
# if true, add the ghost name to the list
# return the list

class variables:
    ghost_list = ["Banshee", "Demon", "Deogen", "Goryo", "Hantu", "Jinn", "Mare", "Moroi", "Myling", "Obake", "Oni", "Onryo", "Phantom", "Poltergeist",
    "Raiju", "Revenant", "Shade", "Spirit", "Thaye", "The Mimic", "The Twins", "Wraith", "Yokai", "Yurei"]
    wish_list = ["• Map information page", "• Special ghost identifiers", "• Cursed object information",
    "• ghost search engine", "• show level requirements per item",
    "• lore command to talk about ghost history"]
    list_list = ['COMMAND LIST', 'help - gives more info on the command',
    'list - shows all commands', 'wave - says hello',
    'evidence - lists what ghost has which evidence', 'wish - lists the current to-do list',
    'map - link to the game maps', 'wiki - link to the game wiki',
    "version - gives the version number", 'level - tells the level of an item',
    'ghost - allows for a lookup for ghosts']
    version = "v0.4 (live)"
    ghost_dictonary = {
        "Banshee": {
            "Evidence": {"DOTS": True,
                "Writing": False,
                "EMF": False,
                "Orbs": True,
                "UV": True,
                "Freezing": False,
                "Spirit": False},
            "speed": 1.7,
            "sanity": "50 (only checks the target)"
        },
        "Demon": {
            "Evidence": {"DOTS": False,
                "Writing": True,
                "EMF": False,
                "Orbs": False,
                "UV": True,
                "Freezing": True,
                "Spirit": False},
            "speed": 1.7,
            "sanity": 70
        },
        "Deogen": {
            "Evidence": {"DOTS": True,
                "Writing": True,
                "EMF": False,
                "Orbs": False,
                "UV": False,
                "Freezing": False,
                "Spirit": True},
            "speed": "When chasing: 3 m/s when far, 0.4 when close. When smudged: 1.6 or lower. It knows the nearest player's location",
            "sanity": 40
        },
        "Goryo": {
            "Evidence": {"DOTS": True,
                "Writing": False,
                "EMF": True,
                "Orbs": False,
                "UV": True,
                "Freezing": False,
                "Spirit": False},
            "speed": 1.7,
            "sanity": 50
        },
        "Hantu": {
            "Evidence": {"DOTS": False,
                "Writing": False,
                "EMF": False,
                "Orbs": True,
                "UV": True,
                "Freezing": True,
                "Spirit": False},
            "speed": "Faster when the house is colder. Lowest is 1.4, highest is 2.7",
            "sanity": 50
        },
        "Jinn": {
            "Evidence": {"DOTS": False,
                "Writing": False,
                "EMF": True,
                "UV": True,
                "Orbs": False,
                "Freezing": True,
                "Spirit": False},
            "speed": "2.5 depending on conditions",
            "sanity": 50
        },
        "Mare": {
            "Evidence": {"DOTS": False,
                "Writing": True,
                "EMF": False,
                "Orbs": True,
                "UV": False,
                "Freezing": False,
                "Spirit": True},
            "speed": 1.7,
            "sanity": "Lights off in ghost room: 60, if Lights on in ghost room: 40."
        },
        "Moroi": {
            "Evidence": {"DOTS": False,
                "Writing": True,
                "EMF": False,
                "Orbs": False,
                "UV": False,
                "Freezing": True,
                "Spirit": True},
            "speed": [1.5, 2.25],
            "sanity": 50
        },
        "Myling": {
            "Evidence": {"DOTS": False,
                "Writing": True,
                "EMF": True,
                "Orbs": False,
                "UV": False,
                "Freezing": True,
                "Spirit": False},
            "speed": 1.7,
            "sanity": 50
        },
        "Obake": {
            "Evidence": {"DOTS": False,
                "Writing": False,
                "EMF": True,
                "Orbs": True,
                "UV": True,
                "Freezing": False,
                "Spirit": False},
            "speed": 1.7,
            "sanity": 50
        },
        "Oni": {
            "Evidence": {"DOTS": True,
                "Writing": False,
                "EMF": True,
                "Orbs": False,
                "UV": False,
                "Freezing": True,
                "Spirit": False},
            "speed": 1.7,
            "sanity": 50
        },
        "Onryo": {
            "Evidence": {"DOTS": False,
                "Writing": False,
                "EMF": False,
                "Orbs": True,
                "UV": False,
                "Freezing": True,
                "Spirit": True},
            "speed": 1.7,
            "sanity": "Always 60 except every thrid flame blown out without other flames near"
        },
        "Phantom": {
            "Evidence": {"DOTS": True,
                "Writing": False,
                "EMF": False,
                "Orbs": False,
                "UV": True,
                "Freezing": False,
                "Spirit": True},
            "speed": 1.7,
            "sanity": 50
        },
        "Poltergeist": {
            "Evidence": {"DOTS": False,
                "Writing": True,
                "EMF": False,
                "Orbs": False,
                "UV": True,
                "Freezing": False,
                "Spirit": True},
            "speed": 1.7,
            "sanity": 50
        },
        "Raiju": {
            "Evidence": {"DOTS": True,
                "Writing": False,
                "EMF": True,
                "Orbs": True,
                "UV": False,
                "Freezing": False,
                "Spirit": False},
            "speed": 2.5,
            "sanity": 65
        },
        "Revenant": {
            "Evidence": {"DOTS": False,
                "Writing": True,
                "EMF": False,
                "Orbs": True,
                "UV": False,
                "Freezing": True,
                "Spirit": False},
            "speed": "1 m/s when it hasn't detected a player. If it detects a player, 3 m/s until it reaches the lask known pos of the player.",
            "sanity": 50
        },
        "Shade": {
            "Evidence": {"DOTS": False,
                "Writing": True,
                "EMF": True,
                "Orbs": False,
                "UV": False,
                "Freezing": True,
                "Spirit": False},
            "speed": 1.7,
            "sanity": "35, unless there is a player in the ghost room (will never hunt)"
        },
        "Spirit": {
            "Evidence": {"DOTS": False,
                "Writing": True,
                "EMF": True,
                "Orbs": False,
                "UV": False,
                "Freezing": False,
                "Spirit": True},
            "speed": 1.7,
            "sanity": 50
        },
        "Thaye": {
            "Evidence": {"DOTS": True,
                "Writing": True,
                "EMF": False,
                "Orbs": True,
                "UV": False,
                "Freezing": False,
                "Spirit": False},
            "speed": "2.75 at youngest, decreasing by 0.175 until it reaches 1.",
            "sanity": "75 at the youngest age, decreasing the sanity threshold by 6 until 15 at the oldest."
        },
        "The Mimic": {
            "Evidence": {"DOTS": False,
                "Writing": False,
                "EMF": False,
                "Orbs": False,
                "UV": True,
                "Freezing": True,
                "Spirit": True},
            "speed": "takes the hunting speed of the ghost it's mimicing",
            "sanity": "takes the hunting sanity of the ghost it's mimicing"
        },
        "The Twins": {
            "Evidence": {"DOTS": False,
                "Writing": False,
                "EMF": True,
                "Orbs": False,
                "UV": False,
                "Freezing": True,
                "Spirit": True},
            "speed": "Main Twin: 1.5, Decoy Twin: 1.9",
            "sanity": 50
        },
        "Wraith": {
            "Evidence": {"DOTS": True,
                "Writing": False,
                "EMF": True,
                "Orbs": False,
                "UV": False,
                "Freezing": False,
                "Spirit": True},
            "speed": 1.7,
            "sanity": 50
        },
        "Yokai": {
            "Evidence": {"DOTS": True,
                "Writing": False,
                "EMF": False,
                "Orbs": True,
                "UV": False,
                "Freezing": False,
                "Spirit": True},
            "speed": 1.7,
            "sanity": "If someone is talking in ghost room: 80, otherwise 50"
        },
        "Yurei": {
            "Evidence": {"DOTS": True,
                "Writing": False,
                "EMF": False,
                "Orbs": True,
                "UV": False,
                "Freezing": True,
                "Spirit": False},
            "speed": 1.7,
            "sanity": 50
        }
    }
    level_dictonary = {
        "flashlight": [1, 19, 35],
        "emf": [1, 20, 52],
        "uv": [1, 21, 56],
        "book": [1, 23, 63],
        "photo": [3, 25, 70],
        "spirit-box": [1, 27, 54],
        "dots": [1, 29, 60],
        "microphone": [7, 31, 72],
        "sound": [11, 32, 58],
        "video": [1, 33, 61],
        "tripod": [10, 34, 62],
        "thermometer": [1, 36, 64],
        "crucifix": [8, 37, 90],
        "meds": [16, 39, 77],
        "igniter": [12, 41, 57],
        "incense": [14, 42, 85],
        "salt": [9, 43, 68],
        "motion": [1, 45, 74],
        "firelight": [12, 47, 79],
        "headgear": [13, 49, 82],
        "level_list": ["flashlight", "emf", "uv", "book", "photo", "spirit-box",
            "dots", "microphone", "sound", "video", "tripod", "thermometer", "crucifix",
            "meds", "igniter", "incense", "salt", "motion", "firelight", "headgear"]
    }
    cursed_object_dictonary = {
        "tarot": {"desc": "Provokes various ghost activities", "actions": ""},
        #"cards": variables.cursed_object_dictonary.get("tarot"),
        "paw": {"desc": "", "actions": ""},
        #"hand": variables.cursed_object_dictonary.get("paw"),
        "voodoo": {"desc": "Forces the ghost to perform interactions", "actions": ""},
        #"doll": variables.cursed_object_dictonary.get("voodoo"),
        "summoning": {"desc": "Teleports the ghost to the circle", "actions": ""},
        #"circle": variables.cursed_object_dictonary.get("summoning"),
        "mirror": {"desc": "Provides a view into the Ghost Room", "actions": "Right click to raise the mirror to see into the ghost room"},
        "ouija": {"desc": "Permits players to ask the ghost various questions", "actions": ""},
        "music": {"desc": "Causes the ghost to sing, broadcasting its current location", "actions": "Right click to play the music box"}
    }

def join_list(list, spacer):
    return spacer.join(map(str, list))

def find_ghost_evidence(trait):
    output_list = []
    for i in range(0, len(variables.ghost_dictonary)):
        current_ghost = variables.ghost_list[i]
        current_evidence = variables.ghost_dictonary.get(current_ghost).get("Evidence")
        if current_evidence.get(trait):
            output_list.append(current_ghost)
    return output_list

def ghost_lookup(ghost, trait):
    ghost_dict = variables.ghost_dictonary
    return ghost_dict.get(ghost).get(trait)

def evidence_list(evidence):
    evidence = evidence.lower()
    if evidence == "list":
        return "DOTS, EMF, Freezing, Orbs, Spirit, UV, Writing"
    if evidence == "dots":
        return find_ghost_evidence("DOTS")
    if evidence == "writing":
        return find_ghost_evidence("Writing")
    if evidence == "emf":
        return find_ghost_evidence("EMF")
    if evidence == "orbs":
        return find_ghost_evidence("Orbs")
    if evidence == "uv":
        return find_ghost_evidence("UV")
    if evidence == "freezing":
        return find_ghost_evidence("Freezing")
    if evidence == "spirit":
        return find_ghost_evidence("Spirit")
    return "I didn't get that evidence... try using the (!evidence list) command to see evidence."

def evidence_compare(evidence, evidence2, evidence3):
    list1 = evidence_list(evidence)
    list2 = evidence_list(evidence2)
    if evidence3 == None:
        list3 = []
        for i in range(0, len(list1)):
            for j in range(0, len(list2)):
                if list1[i] == list2[j]:
                    list3.append(list1[i])
        return join_list(list3, ", ")
    if evidence3 != None:
        list3 = evidence_list(evidence3)
        list4 = []
        for i in range(0, len(list1)):
            for j in range(0, len(list2)):
                for k in range (0, len(list3)):
                    if list1[i] == list2[j] and list2[j] == list3[k]:
                        list4.append(list1[i])
        if len(list4) == 0:
            return "No matching ghost type"
        else:
            return join_list(list4, ", ")

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
    if help == "help":
        return "Welcome to the help command! It tells you about different commands, use this format to learn more about commands ```!help command```"
    if help == "list":
        return "The list command lists the different commands that you can use. It also gives a short description."
    if help == "wave":
        return "I will give you a short wave and a greetings. Nothing of use through :)"
    if help == "evidence":
        return "Allows you to search up ghosts based on a certain type of evidence. The command wihtout parameters will give you the list of evidences. The format for the comamnd is ```!evidence EVIDENCE```"
    if help == "wish":
        return "Gives a short wish list or to-do list of the developer. Feel free to message for more features in the future if it isn't on the list."
    if help == "map":
        return "Gives a link to a map page that has more information on all of the maps in the game."
    if help == "wiki":
        return "Gives a link to the Phasmophobia fan wiki."
    if help == "version":
        return "Gives the version number of the bot. This is used to track which code is being ran."
    if help == "level":
        return """Returns the level needed to get a specific tier for an item. The format is ```!level flashlight```You can also use this command to list the item options ```!level item```You can also list the items based on your level ```!level list 25```"""
    if help == "ghost":
        return """Returns any specific trait that can be looked up. The format is ```!ghost Banshee speed```"""

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!help"):
        if message.content == "!help":
            output = help_list("help")
        else:
            # !help ghost
            help = message.content.split(' ')[1]
            output = help_list(help)
        await message.channel.send(output)

    if message.content.startswith('!list'):
        await message.channel.send("\n".join(map(str,variables.list_list)))

    if message.content.startswith('!wave'):
        await message.channel.send(":wave: Hello, I'm Banshee Bot! You can start using this bot with the commands !list or !help")

    if message.content.startswith('!evidence'):
        command_list = message.content.lower().split(' ')
        output = "error"
        if message.content == "!evidence":
            # !evidence
            output = evidence_list("list")
        if len(command_list) == 2:
            # !evidence emf
            evidence = command_list[1]
            output = join_list(evidence_list(evidence), ", ")
        if len(command_list) == 3:
            # !evidence freezig uv
            evidence = command_list[1]
            evidence2 = command_list[2]
            output = evidence_compare(evidence, evidence2, None)
        if len(command_list) == 4:
            # !evidence writing spirit orbs
            evidence  = command_list[1]
            evidence2 = command_list[2]
            evidence3 = command_list[3]
            output = evidence_compare(evidence, evidence2, evidence3)
        await message.channel.send(output)

    if message.content.startswith("!ghost"):
        command_list = message.content.split(' ')
        output = "error"
        if len(command_list) == 1:
            # !ghost
            output = join_list(variables.ghost_list, ", ")
        else:
            # !ghost Oni
            output = ghost_lookup(command_list[1], command_list[2].lower())
        await message.channel.send(output)


    if message.content.startswith('!level'):
        output = ""
        command_list = message.content.lower().split(' ')
        if len(command_list) == 1:
            # !level
            output = "Please enter the name of the item. Check !help for details."
        if len(command_list) >= 2:
            if command_list[1] == "list":
                # !level list 40
                if len(command_list) > 2:
                    rank = int(command_list[2])
                else:
                    rank = 1
                output = join_list(level_lookup(rank), "\n")
            elif command_list[1] == "item":
                # !level item
                output = join_list(variables.level_dictonary.get("level_list"), ", ")
            else:
                # !level flashlight
                item = command_list[1]
                output = join_list(variables.level_dictonary.get(command_list[1]), ", ")
        await message.channel.send(output)

    if message.content.startswith('!wish'):
        await message.channel.send("\n".join(map(str,variables.wish_list)))

    if message.content.startswith('!map'):
        command_list = message.content.lower().split(' ')
        if message.content.lower() == "!map":
            # !map
            await message.channel.send("https://phasmo.karotte.org/")
        if command_list[1] == "willow":
            # !map willow
            await message.channel.send(help_list(command_list[1]))
            with open('assets/my_file.png', 'rb') as fp:
                await message.channel.send(file=discord.File(fp, 'new_filename.png'))
        else:
            # !map something
            await message.channel.send("https://phasmo.karotte.org/")

    if message.content.startswith('!wiki'):
        await message.channel.send("https://phasmophobia.fandom.com/wiki/Main_Page" )

    if message.content.startswith('!version'):
        await message.channel.send(variables.version)

    if message.content.startswith("!@Banshee Bot"):
        await message.channel.send("no u")

os.system("cls")
f = open("C:\\Tree's Stuff\\discord_tokens\\banshee.json", "r")
client.run(json.loads(f.read()).get("token"))
