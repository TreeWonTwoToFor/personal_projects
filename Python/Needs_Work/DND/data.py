import os
import json

class City:
    def __init__(self, name, location, desc, concept):
        self.name = name
        self.location = location
        self.desc = desc
        self.concept = concept

    def get_dict(self):
        out_dict = {}
        out_dict["Name"] = self.name
        out_dict["Location"] = self.location
        out_dict["Description"] = self.desc
        out_dict["Concept"] = self.concept
        return out_dict
    
class NPC:
    def __init__(self, name, race, age, occupation, location, voice, appearence, personality, goals):
        self.name = name
        self.race = race
        self.age = int(age)
        self.occupation = occupation
        self.location = location
        self.voice = voice
        self.appearence = appearence
        self.personality = personality
        self.goals = goals

    def get_dict(self):
        out_dict = {}
        out_dict["Name"] = self.name
        out_dict["Race"] = self.race
        out_dict["Age"] = self.age
        out_dict["Occupation"] = self.occupation
        if type(self.location) == str:
            out_dict["Location"] = self.location
        elif type(self.location) == City:
            out_dict["Location"] = self.location.name
        out_dict["Voice"] = self.voice
        out_dict["Appearence"] = self.appearence
        out_dict["Personality"] = self.personality
        out_dict["Goals"] = self.goals
        return out_dict


def clear():
    os.system('cls')

def read():
    global json_dict
    try:
        with open(in_file, 'r') as file:
            json_dict = json.load(file)
    except:
        raise FileNotFoundError("Something went wrong in the file reading process.")

def write():
    global json_dict
    with open(out_file, 'w') as file:
        json.dump(json_dict, file, indent=4)

clear()
# should be something like "data1"
in_file = input("Please input the file name w/o the file extension: ")
try:
    out_file = in_file[:-1] + str(int(in_file[-1])+1) + ".json" # data2.json
except:
    raise ValueError("The file must end with a number")
in_file = in_file + ".json" # data1.json
read()

running = True
while running:
    print("What do you want to add?\n1. City\n2. NPC")
    user_input = input(" > ").lower()
    if user_input in ["1", "city"]:
        city_name = input("What is the name of your city?\n > ")
        city_latitude = input("Where is this city (latitude)?\n > ")
        city_longitude = input("(longitude)?\n > ")
        city_desc = input("What is this city like?\n > ")
        city_concept = input("What is the main idea of this city?\n > ")
        city = City(city_name, [int(city_latitude),int(city_longitude)], city_desc, city_concept)
        json_dict["City"][city_name] = city.get_dict()
    elif user_input in ["2", "npc"]:
        npc_name = input("What is the name of this NPC?\n > ")
        npc_race = input("What is their race?\n > ")
        npc_age = input("How old are they?\n > ")
        npc_occupation = input("What is their occupation/role?\n > ")
        npc_location = input("Where have/will the party find them?\n > ")
        npc_voice = input("What do they sound like?\n > ")
        npc_appearence = input("What do they look like?\n > ")
        npc_personality = input("What is their personality like?\n > ")
        npc_goals = input("What are their goals?\n > ")
        npc = NPC(npc_name, npc_race, npc_age, npc_occupation, npc_location, npc_voice, npc_appearence, npc_personality, npc_goals)
        json_dict["NPC"][npc_name] = npc.get_dict()
    user_continue = input("Do you wish to add more (y/n)?\n > ").lower()
    clear()
    if user_continue in ["n", "no"]:
        write()
        running = False