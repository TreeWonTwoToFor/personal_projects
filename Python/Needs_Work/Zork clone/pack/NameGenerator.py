import random

consonant_list = ["g", "th","d","r","k","b","v"]
vowel_list = ["o", "e", "a"]

def random_consonant():
    con = consonant_list[random.randint(0, len(consonant_list)-1)]
    return con

def random_vowel():
    vow = vowel_list[random.randint(0, len(vowel_list)-1)]
    return vow

def random_diphone():
    diphone = random_consonant() + random_vowel()
    return diphone

def random_name(syllables):
    output = ""
    for i in range(syllables):
        output += random_diphone()
    return output.capitalize()