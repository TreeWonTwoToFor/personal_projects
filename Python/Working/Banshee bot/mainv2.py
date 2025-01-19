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

class Ghost:
    def __init__(self, name, speed, evidence_list, hunt_sanity, strength, weakness, tells, wiki):
        self.name = name
        self.speed = speed
        self.evidence_list = evidence_list
        self.hunt_sanity = hunt_sanity
        self.strength = strength
        self.weakness = weakness
        self.tells = tells
        self.wiki = wiki

    def simple_output(self):
        output = f"Details about {self.name}:```Speed: {self.speed}m/s"
        output += f"\nEvidence: {join_list(self.evidence_list, ', ')}"
        output += f"\nHunt Sanity: {self.hunt_sanity}%"
        output += f"\nStength: {self.strength}"
        output += f"\nWeakness: {self.weakness}"
        output += f"\nTells: {self.tells}```"
        output += f"\nWiki link: {self.wiki}"
        return output


ghost_dict = {
    "Spirit":  Ghost("Spirit", 1.7, ["EMF", "Spirit Box", "Writing"], 
            50, None, "A Spirit can be temporarily stopped by burning INcense near them.",
            "Incense will stop it from hunting for double the time (180s compared to 90s).",
            "https://phasmophobia.fandom.com/wiki/Spirit"),
    "Wraith": Ghost("Wraith", 1.7, ["EMF", "Spirit Box", "DOTs"],
            50, "Wraiths almost never touch the ground, meaning it can't be tracked by footsteps", 
            "Wraiths are afraid of Salt, and will actively avoid it.",
            "Wraiths will not step in salt, and T3 salt will not slow them down.",
            "https://phasmophobia.fandom.com/wiki/Wraith"),
    "Phantom": Ghost("Phantom", 1.7, ["Spirit Box", "UV", "DOTs"],
            50, "Looking at a Phantom will drop your sanity considerably faster.",
            "Taking a photo of the Phantom will make it temporarily disappear.",
            "The weakness, along with longer blinks while it's visible.",
            "https://phasmophobia.fandom.com/wiki/Phantom"),
    "Poltergeist": Ghost("Poltergeist", 1.7, ["Spirit Box", "UV", "Ghost Writing"],
            50, "Poltergeists can throw multiple objects at once, and with great force.", 
            "With nothing to throw, Poltergeists become powerless.",
            "The multi-throw event is unique to Poltergeists.",
            "https://phasmophobia.fandom.com/wiki/Poltergeist"),
    "Banshee": Ghost("Banshee", 1.7, ["UV", "Ghost Orbs", "DOTs"],
            "12-50-87", "Banshees will weaken their target before striking.", 
            "Banshees can sometimes be heard screaming with a parabolic microphone.",
            "Banshees focus only on their target player if they are in the house. This means that other players will be safe during hunts, and that hunts can trigger at a higher average sanity.",
            "https://phasmophobia.fandom.com/wiki/Banshee"),
    "Jinn": Ghost("Jinn", "1.7-2.5", ["EMF", "UV", "Freezing"],
            50, "A Jinn will travel at a faster speed if its victim is far away.", 
            "Turning off the location's power source will prevent the Jinn from using its ability.",
            "It cannot turn off the breaker, and the speed changes depending on LOS, breaker state, and distance from player.",
            "https://tybayn.github.io/phasmo-cheat-sheet/"),
    "Mare": Ghost("Mare", 1.7, ["Spirit Box", "Ghost Orbs", "Writing"],
            "40/60", "A Mare will have an increased chance to attack in the dark.", 
            "Turning the lights on around the Mare will lower its chance to attack.",
            "It can turn off the light practically instantly after a players turns it on.",
            "https://phasmophobia.fandom.com/wiki/Mare"),
    "Revenant": Ghost("Revenant", "1.0-3.0", ["Ghost Orbs", "Writing", "Freezing"],
            50, "A Revanant will travel at a significantly faster speed when hunting their prey.", 
            "Hiding from the Revenant will cause it to move very slowly.",
            "The massive speed change is very deadly, but a very clear tell.",
            "https://phasmophobia.fandom.com/wiki/Revenant"),
    "Shade": Ghost("Shade", 1.7, ["EMF", "Writing", "Freezing"],
            35, "Shades are much harder to find.", 
            "The ghost will not enter a hunt if there are people nearby."
            "It's weakness, and it's very low activity.",
            "https://phasmophobia.fandom.com/wiki/Shade"),
    "Demon": Ghost("Demon", 1.7, ["UV", "Writing", "Freezing"],
            "70/100", "Demons will initiate hunts more often than other ghosts.", 
            "Demons fear the crucifix and will be less aggressive near one.",
            "It's aggressive nature (less than 25 second hunt cooldown), and the lower inscense duration (60s instead of 90s).",
            "https://phasmophobia.fandom.com/wiki/Demon"),
    "Yurei": Ghost("Yurei", 1.7, ["Ghost Orbs", "Freezing", "DOTs"],
            50, "Yureis have been known to have a stronger effet on people's sanity.", 
            "Smudging the Yurei's place of death will trap it temporarily, reducing how much it wanders.",
            "They can interact with the exit door without hunting/eventing. They can fully shut any door.",
            "https://phasmophobia.fandom.com/wiki/Yurei"),
    "Oni": Ghost("Oni", 1.7, ["EMF", "Freezing", "DOTs"],
            50, "Oni are more active whilsts people are nearby and will drain their sanity faster when manifesting.", 
            "Oni disappear less often while hunting their prey.",
            "Cannot perform the airball event, and has double the sanity drain.",
            "https://phasmophobia.fandom.com/wiki/Oni"),
    "Yokai": Ghost("Yokai", 1.7, ["Spirit Box", "Ghost Orbs", "DOTs"],
            "50/80", "Talking near a Yokai will anger it, increasing the chance of an attack.", 
            "When hunting, a Yokai can only hear voices clost to it.",
            "The ability to detect players is lowered, but if it can it becomes stronger. Try talking around it to see it's responce.",
            "https://phasmophobia.fandom.com/wiki/Yokai"),
    "Hantu": Ghost("Hantu", "1.4-2.7", ["UV", "Ghost Orbs", "Freezing"],
            50, "Lower temperatures allow the Hantu to move at faster speeds.", 
            "Hantus move slower in warmer areas.",
            "Does NOT have LOS speed increase, and they tend to be stronger near the ghost room.",
            "https://phasmophobia.fandom.com/wiki/Hantu"),
    "Goryo": Ghost("Goryo", 1.7, ["EMF", "UV", "DOTs"],
            50, "A Goryo will usually only show itself on camera if there are no people nearby.", 
            "They are rarely seem far from their place of death",
            "DOTs only appears on video camera",
            "https://phasmophobia.fandom.com/wiki/Goryo"),
    "Myling": Ghost("Myling", 1.7, ["EMF", "UV", "Writing"],
            50, "A Myling is known to be quieter when hunting.", 
            "Mylings make more frequent paranormal sounds.",
            "Their strength is a double-edged sword, as Mylings are the only 'quiet' ghost in the game.",
            "https://phasmophobia.fandom.com/wiki/Myling"),
    "Onryo": Ghost("Onryo", 1.7, ["Spirit Box", "Ghost Orbs", "Freezing"],
            "60/100", "Every thrid firelight causes an Onryo to attack.", 
            "When threatened, this ghost will be less likely to hunt.",
            "Onryo's are averted to flames, so using those are not only important for safety, but also for identification."
            "https://phasmophobia.fandom.com/wiki/Onryo"),
    "The Twins": Ghost("The Twins", "1.53-1.87", ["EMF", "Spirit Box", "Freezing"],
            50, "Either twin can be angred, and attack it's prey.", "They will often interact at the same time."
            "'Twinteractions' are a strong identifier. Also having multiple interactions in different places may help.",
            "https://phasmophobia.fandom.com/wiki/The_Twins"),
    "Raiju": Ghost("Raiju", "1.7-2.5", ["EMF", "Ghost Orbs", "DOTs"],
            "50/65", "A Raiju can siphon power from nearby electrical devices, making it move faster.", 
            "Constantly dirsupts electronic equipment, making it easier to track.",
            "Since electrical equipment plays a big role, testing if player equipment affects the ghost is a great metric.",
            "https://phasmophobia.fandom.com/wiki/Raiju"),
    "Obake": Ghost("Obake", 1.7, ["EMF", "UV", "Ghost Orbs"],
            50, "When interacting with the environment, and Obake will rarely leave a trace.", 
            "Sometimes this ghost will shapeshift, leaving behind unique evidence.",
            "Because of it's shapeshifting, it can be identified by it's fingerprints, and it's ghost model",
            "https://phasmophobia.fandom.com/wiki/Obake"),
    "The Mimic": Ghost("The Mimic", 1.7, ["Spirit Box", "UV", "Freezing"],
            "12/50/100", "We're unsure what this ghost is capable of. Be careful.", 
            "Several reports have noted ghost orb sightings near mimics.",
            "It's chaning behaviour (every 30s-2m) is important for identification. It also can show 4 evidences (the extra being ghost orbs).",
            "https://phasmophobia.fandom.com/wiki/The_Mimic"),
    "Moroi": Ghost("Moroi", "(3.71 LOS) 1.5-2.25", ["Spirit Box", "Writing", "Freezing"],
            50, "The weaker the victims, the stronger the Moroi becomes.", 
            "Moroi suffer from hypersomia, weakening them for longer periods.",
            "Because of it's curse through Spirit Box or Parabolic Microphone, it unequally drains sanity. It also gets faster the lower the players' sanity.",
            "https://phasmophobia.fandom.com/wiki/Moroi"),
    "Deogen": Ghost("Deogen", "0.4-3.0", ["Spirit Box", "Writing", "DOTs"],
            40, "Deogens constantly sense the living. You can run but you can't hide.", 
            "Deogens require a lot of energy to form, and will mover very slowly wen approaching its victim.",
            "It's speed is the strongest tell, along with it being able to always find the player.",
            "https://phasmophobia.fandom.com/wiki/Deogen"),
    "Thaye": Ghost("Thaye", "1.0-2.75", ["Ghost Orbs", "Writing", "DOTs"],
            "15/75", "Upon entering the location, Thaye will become active, defensive and agile.", 
            "Thaye weaken over time, making them weaker, slower, and less aggressive.",
            "It's high speed, not getting more speed from LOS, and aging are the strongest tells.",
            "https://phasmophobia.fandom.com/wiki/Thaye")
}

class variables:
    ghost_list = ["Banshee", "Demon", "Deogen", "Goryo", "Hantu", "Jinn", "Mare", "Moroi", "Myling", "Obake", "Oni", "Onryo", "Phantom", "Poltergeist",
    "Raiju", "Revenant", "Shade", "Spirit", "Thaye", "The Mimic", "The Twins", "Wraith", "Yokai", "Yurei"]
    to_do_list = ["• Special ghost identifiers", "• Cursed object information",
    "• show level requirements per item", "• Sound Clips for parabolic microphone + walking speed",
    "• lore command to talk about ghost history"]
    to_do_list.sort()
    list_list = ['COMMAND LIST', 'help - gives more info on the command',
    'list - shows all commands', 'wave - says hello',
    'evidence - lists what ghost has which evidence', 'to-do - lists the current to-do list',
    'map - link to the game maps', 'wiki - link to the game wiki',
    "version - gives the version number", 'level - tells the level of an item',
    'ghost - allows for a lookup for ghosts']
    list_list.sort()
    version = "v0.5 (live)"
    evidence_list = ["EMF", "UV", "DOTs", "Ghost Orbs", "Ghost Writing", "Freezing", "Spirit Box"]
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
    map_list = ["Ridgeview Court", "Willow Street", "Edgeview Road", "Tanglewood Drive", 
                "Bleasedale Farmhouse", "Brownstone High School", "Camp Woodwind", "Grafton Farmhouse", 
                "Maple Lodge Campsite", "Point Hope", "Prison", "Sunny Meadowns Mental Institution"]

def join_list(list, spacer):
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
            await message.channel.send('```'+join_list(variables.list_list, "\n")+'```')
        case "!wave":
            await message.channel.send(":wave: Hello, I'm Banshee Bot! You can start using this bot with the commands !list or !help")
        case "!to-do" | "!todo":
            await message.channel.send(join_list(variables.to_do_list, "\n"))
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
        case "!help":
            try:
                await message.channel.send(help_list(command_list[1]))
            except:
                await message.channel.send("Please enter a valid command to ask for help on.")
        case "!level":
            output = ""
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
        case "!evidence":
            if len(command_list) == 1:
                await message.channel.send('```' + join_list(variables.evidence_list, "\n") + '```')
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
                elif "farmhouse" in command_list:
                    if "bleasedale" in command_list:
                        await message.channel.send('https://phasmo.karotte.org/maps/bleasdale-farmhouse/')
                    elif "grafton" in command_list:
                        await message.channel.send('https://phasmo.karotte.org/maps/grafton-farmhouse/')
                    else:
                        await message.channel.send("I'm unsure which farmhouse you are talking about. Use 'bleasedale', or 'grafton'.")
                else:
                    await message.channel.send("I'm unsure which house you are talking about. Use '!map list' if you want the names of the maps.")
                

os.system("cls")
f = open("C:\\JSGames\\discord_tokens\\banshee.json", "r")
client.run(json.loads(f.read()).get("token"))
