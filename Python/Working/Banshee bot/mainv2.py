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
        output += f"Wiki link: {self.wiki}"
        return output

class Item:
    def __init__(self, name, item_type, desc, tier=0, max_limit=1, level=0):
        self.name = name
        self.desc = desc
        self.item_type = item_type
        self.tier = tier
        self.level = level

    def simple_output(self):
        return f"Tier {self.tier} {self.name}:```{self.desc}```"

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
            "The ghost will not enter a hunt if there are people nearby.",
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
            "The ability to detect players is lowered, but if it can it becomes stronger. Try talking around it to see it's response.",
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
            "Onryo's are averted to flames, so using those are not only important for safety, but also for identification.",
            "https://phasmophobia.fandom.com/wiki/Onryo"),
    "The Twins": Ghost("The Twins", "1.53-1.87", ["EMF", "Spirit Box", "Freezing"],
            50, "Either twin can be angred, and attack it's prey.", "They will often interact at the same time.",
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

item_dict = {
    "list": ["DOTs Projector", "EMF Reader", "Ghost Writing Book", "Spirit Box", "Thermometer", "UV Light", "Video Camera", "Flashlight",
            "Head Gear", "Igniter", "Incense", "Motion Sensor", "Parabolic Microphone", "Photo Camera", "Salt", "Sanity Medication", "Sound Sensor",
            "Tripod", "Objective Board", "Site Map", "Sanity Monitor", "Site Activity Monitor", "Computer", "Sound Monitor", "Clipboards",
            "Bones", "Haunted Mirror", "Monkey Paw", "Music Box", "Ouija Board", "Summoning Circle", "Tarot Cards", "Voodoo Doll"],
    "DOTs Projector":  [Item("DOTs Projector", "Starter Equipment", 
                            "The DOTs Pen projects green dots from it's position on the floor or in the player's hand in a 5 meter narrow cone. When the ghost is in DOTs mode, and in the cone's range, the ghost's model will appear.", 1, 2, 0),
                        Item("DOTs Projector", "Starter Equipment", 
                            "This DOTs Projector must be placed onto the floor, wall, or ceiling. It has a smaller range of 2.5 meters, however it's circular area makes it much easier to cover a full hallway, or section of the room.", 2, 2, 29),
                        Item("DOTs Projector", "Sterter Equipment",
                            "A motorized projector which can cover entire rooms. It's range of 7 meters, wide spotlight, and it's scanning capabilities make this DOTs projecter very strong.", 3, 2, 60)],
    "EMF Reader":  [Item("EMF Reader", "Starter Equipment",
                        "This starter EMF Reader can show the Electro-magnetic Frequencies that ghosts emit by interacting with the lights, objects in the room, and by causing events. This EMF Reader isn't very accurate, and only has a range of 1.7 meters.",1,2),
                    Item("EMF Reader", "Starter Equipment", 
                        "This tier of EMF Reader has multiple upgrades over the previous tier of reader. First, it now has an audio indicator, which gives you a good idea of which EMF level the ghost emitted. Second, the 2 meter range makes it easier to set down, and check when you hear it blaring. Finally, it's increased accuracy makes it more consistent during gameplay.", 2, 2, 20),
                    Item("EMF Reader", "Starter Equipment", 
                        "A custom-made device with the special purpose of identifying and locating ghosts. It's display shows up to three interactions with high accuracy, and a pointer towards it's origin. It's increased range of 3.5 meters significantly boosts it's effectiveness.", 3, 2, 52)],
    "Ghost Writing Book":  [Item("Ghost Writing Book", "Starter Equipment", 
                                "A simple notebook and pencil which get the job done, even if it doesn't look too special. It's range of 3 meters, along with it's low interaction rate leave much to be desired.", 1, 2),
                            Item("Ghost Writing Book", "Starter Equipment", 
                                "A leather case covering these parchment pages are more appealing to write on, making the ghost more interested in writing in this book to share it's message. With an increased range of 4 meters, and a medium interaction rate, this book is a significant upgrade.", 2, 2, 23),
                            Item("Ghost Writing Book", "Starter Equipment", 
                                "This grimoire has a lot of history, with metalic accents that the ghost cannot resist. It's range of 5 meters, and highest interaction rate make it by far the strongest of the three options.d", 3, 2, 63)],
    "Spirit Box":  [Item("Spirit Box", "Starter Equipment", 
                        "This old FM/AM radio with a tinny speaker makes it hard to hear what the ghost wants to say. It's range of 3 meters, and low response leave much to wish for.", 1, 2, 0),
                    Item("Spirit Box", "Starter Equipment", 
                        "This Spirit Box is solely built for conversations with the unknown. It's modern design make it much easier for the ghost to hear you, and for you to hear it. It's 4 meter range is also a nice upgrade.", 2, 2, 27),
                    Item("Spirit Box", "Starter Equipment", 
                        "It's ability to scan two frequency channels at the same time make it the best option. It's high response rate, and audio quality at an increased range of 5 meters make it the expert's choice.", 3, 2, 54),],
    "Thermometer": [Item("Thermometer", "Starter Equipment", 
                        "This vintage wall thermometer is quite slow, and can be inaccurate. However, it works perfectly fine for just carrying it around and measuring the temperature.", 1, 2),
                    Item("Thermometer", "Starter Equipment", 
                        "A medical grade thermometer, which can quickly identify the temperature to a higher accuracy. It's electronic readings do seem to sometimes be a little off.", 2, 2, 36),
                    Item("Thermometer", "Starter Equipment", 
                        "More modern, more technical, and more accurate. You just can’t beat it.", 3, 2, 64)],
    "UV Light":[Item("UV Light", "Starter Equipment", 
                    "A small flashlight that after a few seconds can show fingerprints and footsteps from the ghost. It's narrow spotlight can cause issues.", 1, 2, 0),
                Item("UV Light", "Starter Equipment", 
                    "This glowstick can light up a significant area around it, making it easier to set down and have it do it's job. It does need to be shaken every minute to keep emitting light, and it doubles the charge time of nearby tracks, but some like it better than the flashlights.", 2, 2, 21),
                Item("UV Light", "Starter Equipment", 
                    "This Pro UV Light can illuminate massive areas with light. It's short charge time, and wide spotlight make it a great option.", 3, 2, 56)],
    "Video Camera":[Item("Video Camera", "Starter Equipment", 
                        "A camera that was laying around in the old office, which hopefully should get the job done. It does have some cool nightvision, but the screen is quite small, and it seems to be glitchy around ghosts.", 1, 4),
                    Item("Video Camera", "Starter Equipment", 
                        "This new Parasonic camera is a bit nicer than the old Bony camcorder, with better image quality, and doesn't glitch out as much.", 2, 4, 33),
                    Item("Video Camera", "Starter Equipment", 
                        "Bony's new state-of-the-art camera created solely for ghost hunters. It's image quality, and lack of almost any glitches make it a strong contender for best camera.", 3, 4, 61)],
    "Flashlight":  [Item("Flashlight", "Starter Equipment", 
                        "It's surprising that this flashlight still works, with it's low intensity and narrow beam. Still, it works.", 1, 4, 0),
                    Item("Flashlight", "Starter Equipment", 
                        "A real, modern flashlight. It still has a narrow beam, but it's much brighter than the old ones we used to use.", 2, 4, 19),
                    Item("Flashlight", "Starter Equipment", 
                        "This light is a beast, with a huge spotlight and high intensity, it feels like I can see everything!", 3, 4, 35)],
    "Crucifix":[Item("Crucifix", "Optional Equipment", 
                    "Just two twigs tied together. It's shape alone stops the paranormal. It's range of 3 meters, and single use does mean it isn't very effective.", 1, 2, 8),
                Item("Crucifix", "Optional Equipment", 
                    "A cast iron cross, which has a stronger influence over the ghost. It's increased range of 4 meters and 2 uses make it a significant improvement.", 2, 2, 37),
                Item("Crucifix", "Optional Equipment", 
                    "An ornate cross made with gold and silver has proven to be a strong defence against other wordly beings. It's range of 5 meters, and it's ability to prevent a cursed hunt makes it the expert chioce.", 3, 2, 90)],
    "Firelight":   [Item("Firelight", "Optional Equipment", 
                        "A small little candle in a rusting candleholder. It's range of 2 meters, duration of 5 minutes, and it's 33% reduced sanity drain make it a useful, albeit mediocre, defense.", 1, 4, 12),
                    Item("Firelight", "Optional Equipment", 
                        "This candelabra with three tall candles attached. The higher quality candle wax adds several benfits, like double the duration (10 minutes), as well as a higher Sanity Conservation (33% -> 50%).", 2, 4, 47),
                    Item("Firelight", "Optional Equipment", 
                        "A gasoline fuelled lantern, which has been found to be one of the most reliable sources. Due to it being waterproof, and it's increased Sanity Drain protection (50% -> 66%) make it the best option for a natural light source.", 3, 4, 79)],
    "Head Gear": [Item("Head Gear", "Optional Equipment", 
                      "A GhostPro camera mounted to some head straps. It has a medium image quality, and it's paranormal activity being relatively low make it a fine option.", 1, 4, 13),
                  Item("Head Gear", "Optional Equipment", 
                      "A small flashlight attached to the player's head. It is basically the equivalent of the Tier 2 flashlight, but on your head!", 2, 4, 49),
                  Item("Head Gear", "Optional Equipment", 
                      "Military grade night vision goggles. While it has high paranormal interference, it's night vision capabilities make it the best visibility option in the game.", 3, 4, 82)],
    "Igniter": [Item("Igniter", "Optional Equipment", 
                    "A small little matchbox with a ghost as it's mascot. Each match lasts 10 seconds, and there are 10 matches in the box.", 1, 4, 12),
                Item("Igniter", "Optional Equipment", 
                    "A small, compact gas lighter. With a duration of 5 minutes, it's much more convenient than the matchbox.", 2, 4, 41),
                Item("Igniter", "Optional Equipment", 
                    "A high quality Zippy Lighter, which has double the duration of the previous lighter (5m -> 10m), and it's waterproof!", 3, 4, 57)],
    "Incense": [Item("Incense", "Optional Equipment", 
                     "A small bundle of black sage. It has a range of 3 meters, duration of 5 seconds, and blinds the ghost during the hunt for 5 seconds.", 1, 4, 14),
                Item("Incense", "Optional Equipment", 
                     "A large bundle of white sage, with a nice string to tie it together. It has an increased range of 4 meters, a 6 second duration, and slows the ghost during hunts for 5 seconds.", 2, 4, 42),
                Item("Incense", "Optional Equipment", 
                     "A holy incense burner which does a great job warding off paranormal entities. With a range of 5 meters, 7 second duration, an the ability to blind and stop the ghost, it's a very strong option.", 3, 4, 85)],
    "Motion Sensor": [Item("Motion Sensor", "Optional Equipment", 
                           "A wildlife camera that's been modified to track the paranormal. It's sensor shape is a line, and has a light indicator for when the sensor is tripped.", 1, 4, 5),
                      Item("Motion Sensor", "Optional Equipment", 
                           "A modified version of the previous motion sensor, which has new shapes, as well as an audio indicator.", 2, 4, 45),
                      Item("Motion Sensor", "Optional Equipment", 
                           "A security camera with a range of 1.5 meters, which can track anything in the space around it.", 3, 4, 74)],
    "Parabolic Microphone": [Item("Parabolic Microphone", "Optional Equipment", 
                                  "Allows the user to hear sounds up to 20 meters way, and with a better clarity than the naked ear.", 1, 2, 7),
                             Item("Parabolic Microphone", "Optional Equipment", 
                                  "An upgraded and improved version of the previous parabolic microphone! It's range of 30 meters, as well as a small screen, makes it a nice quality of live upgrade.", 2, 2, 31),
                             Item("Parabolic Microphone", "Optional Equipment", 
                                  "A high quality microphone that not only gives you the sound the ghosts makes, but also tells you where it comes from.", 3, 2, 72)],
    "Photo Camera": [Item("Photo Camera", "Optional Equipment", 
                          "An old polteroid camera, which takes a few seconds to print the picture (3 seconds between images).", 1, 3, 3),
                     Item("Photo Camera", "Optional Equipment", 
                          "A Bony digital camera, which speeds up the picurre taking process. It takes 2 seconds to process the image, and gives you a nice digital screen to see what the photo looks like. However, it does get glitchy around ghosts.", 2, 3, 25),
                     Item("Photo Camera", "Optional Equipment", 
                          "The new flagship Bony camera, which not only resists the paranormal better, but also cuts the time between photos in half (1 second instead of 2).", 3, 3, 70)],
    "Salt": [Item("Salt", "Optional Equipment", 
                  "A two use container of Ghost Huntin' Distribution's very own brand of Salt.", 1, 3, 9),
             Item("Salt", "Optional Equipment", 
                  "A three use container of pink Himalayan salt that is great for revealing footprints. It's long lines make it eaiser to block wider passages.", 2, 3, 43),
             Item("Salt", "Optional Equipment", 
                  "A glass bottle of blessed black salt, which not only has 3 salt uses per bottle, but also slows the ghost down during hunts.", 3, 3, 68)],
    "Sanity Medication": [Item("Sanity Medication", "Optional Equipment", 
                               "A bottle of Insane Away, which holds vintage snake oil, can be drunk to restore a portion of your sanity. It gives you 20 seconds of sanity restoration (the % depneds on the difficulty).", 1, 4, 16),
                          Item("Sanity Medication", "Optional Equipment", 
                               "A more regulated pill bottle that restores your sanity faster. It cuts the restoration speed in half (20s -> 10s).", 2, 4, 39),
                          Item("Sanity Medication", "Optional Equipment", 
                               "A new formula which must be injected, which gives you an adrenaline dump, causing the player to get a 10 second sprint boost.", 3, 4, 77)],
    "Sound Sensor": [Item("Sound Sensor", "Optional Equipment", 
                          "", 1, 4, 11),
                     Item("Sound Sensor", "Optional Equipment", 
                          "", 2, 4, 32),
                     Item("Sound Sensor", "Optional Equipment", 
                          "", 3, 4, 58),],
    "Tripod": Item("Tripod", "Optional Equipment", ""),
    "Objective Board": Item("Objective Board", "Truck Equipment", ""),
    "Site Map": Item("Site Map", "Truck Equipment", ""),
    "Sanity Monitor": Item("Sanity Monitor", "Truck Equipment", ""),
    "Site Activity Monitor": Item("Site Activity Monitor", "Truck Equipment", ""),
    "Computer": Item("Computer", "Truck Equipment", ""),
    "Sound Monitor": Item("Sound Monitor", "Truck Equipment", ""),
    "Clipboards": Item("Clipboards", "Truck Equipment", ""),
    "Bones": Item("Bones", "House Item", ""),
    "Haunted Mirror": Item("Haunted Mirror", "House Item", ""),
    "Monkey Paw": Item("Monkey Paw", "House Item", ""),
    "Music Box": Item("Music Box", "House Item", ""),
    "Ouija Board": Item("Ouija Board", "House Item", ""),
    "Summoning Circle": Item("Summoning Circle", "House Item", ""),
    "Tarot Cards": Item("Tarot Cards", "House Item", ""),
    "Voodoo Doll": Item("Voodoo Doll", "House Item", "")
}

class variables:
    ghost_list = ["Banshee", "Demon", "Deogen", "Goryo", "Hantu", "Jinn", "Mare", "Moroi", "Myling", "Obake", "Oni", "Onryo", "Phantom", "Poltergeist",
    "Raiju", "Revenant", "Shade", "Spirit", "Thaye", "The Mimic", "The Twins", "Wraith", "Yokai", "Yurei"]
    to_do_list = ["• Cursed object information", "• Make level command more robust",
    "• Show level requirements per item", "• Sound Clips for parabolic microphone + walking speed",
    "• Lore command to talk about ghost history", "• Add tiers to the items in the level list"]
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
    map_list = ["Ridgeview Court", "Willow Street", "Edgeview Road", "Tanglewood Drive", 
                "Bleasedale Farmhouse", "Brownstone High School", "Camp Woodwind", "Grafton Farmhouse", 
                "Maple Lodge Campsite", "Point Hope", "Prison", "Sunny Meadowns Mental Institution"]

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
        case "!help":
            if len(command_list) == 1:
                await message.channel.send(join_list(variables.list_list, "\n", True))
            else:
                try:
                    await message.channel.send(help_list(command_list[1]))
                except:
                    await message.channel.send(help_list("Please make sure to enter a valid command"))
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
        case "!item":
            try:
                await message.channel.send(item_dict[command_list[1].capitalize()][0].simple_output())
            except:
                await message.channel.send("Please enter a valid name")
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
# f = open("C:\\Tree's Stuff\\discord_tokens\\banshee.json", "r")
client.run(json.loads(f.read()).get("token"))
