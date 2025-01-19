import os

def clear(): os.system('cls')

def title(string): print("-"*20+"\n"+string+"\n"+"-"*20)

clear()

class Phoneme:
    def __init__(self, character, is_vowel, manner=None, place=None):
        self.IPA = character
        self.is_vowel = is_vowel
        if not is_vowel:
            self.manner = manner
            self.place = place

    def __eq__(self, other):
        if type(other) == str:
            return other == self.IPA
        elif type(other) == Phoneme:
            return other.IPA == self.IPA

    def print(self):
        if self.is_vowel:
            print(self.IPA)
        else:
            print(self.IPA, ": ", self.manner, self.place)


phoneme_dict = {
    'p': Phoneme('p', False, 'Plosive', 'Bilabial'),
    'b': Phoneme('b', False, 'Plosive', 'Bilabial'),
    'bb': Phoneme('B', False, 'Trill', 'Bilabial'),
    'f': Phoneme('f', False, 'Fricative', 'Labio-dental'),
    'v': Phoneme('v', False, 'Fricative', 'Labio-dental'),
    'ϴ': Phoneme('ϴ', False, 'Fricative', 'Dental'),
    '|': Phoneme('|', False, 'Click', 'Dental'),
    't': Phoneme('t', False, 'Plosive', 'Alveolar'),
    'd': Phoneme('d', False, 'Plosive', 'Alveolar'),
    's': Phoneme('s', False, 'Fricative', 'Alveolar'),
    'z': Phoneme('z', False, 'Fricative', 'Alveolar'),
    'r': Phoneme('ɹ', False, 'Approximate', 'Alveolar'),
    'l': Phoneme('ɾ', False, 'Tap', 'Alveolar'),
    'rr': Phoneme('r', False, 'Trill', 'Alveolar'),
    '||': Phoneme('||', False, 'Click', 'Alveolar'),
    'h': Phoneme('h', False, 'Fricative', 'Glottal'),
    'a': Phoneme('a', True),
    'i': Phoneme('i', True),
    'u': Phoneme('u', True),
    'o': Phoneme('o', True),
    'e': Phoneme('ə', True)
}

vowel_list = ['a', 'i', 'u', 'o', 'ə']

consonant_list = ['p', 'b', 'B', 'f', 'v', 
                  'ϴ', '|', 't', 'd', 's',
                  'z', 'ɹ', 'ɾ', 'r', '||',
                  'h']

# this diphthong list doesn't include long vowels
diphthong_list = []
for i in range(4):
    first_vowel = vowel_list[i]
    for j in range(4):
        if vowel_list[j] is not first_vowel:
            second_vowel = vowel_list[j]
            diphthong_list.append(first_vowel+second_vowel)

neucleus_list = vowel_list + diphthong_list 

word_list = {}

count = 0
title("Single Onset") # for example, hu
for consonant in consonant_list:
    for vowel in neucleus_list:
        count += 1
        print(f"{count}: {consonant+vowel}")
        word_list[count] = consonant+vowel
num_single_onset_end = count

title("Single Coda") # for example, ib
invalid_coda = ['|', '||']
for consonant in consonant_list:
    if consonant not in invalid_coda:
        for vowel in neucleus_list:
            count += 1
            print(f"{count}: {vowel+consonant}")
            word_list[count] = vowel+consonant
num_single_coda_end = count

print(len(word_list))
for i in range(num_single_onset_end, num_single_coda_end):
    for constant in consonant_list:
        count += 1 
        word_list[count] = consonant + word_list[i+1]
        print(f"{count}: {consonant + word_list[i+1]}")

title("Single Oneset and Single Coda") # for example, ret
invalid_coda = ['|', '||']
for consonant_b in consonant_list:
    if consonant not in invalid_coda:
        for cononant_a in consonant_list:
            for vowel in neucleus_list:
                count += 1
                #print(f"{count}: {cononant_a+vowel+consonant_b}")

# title("Dual Coda") # for example, ugt
# invalid_coda = ['|', '||', 'B', 'r'] # clicks aren't valid at all, and trills must be mono-phonemic
# for consonant_a in consonant_list:
#     if not consonant_a in invalid_coda:
#         for consonant_b in consonant_list:
#             if not consonant_b in invalid_coda:
#                 # both consonants are valid ending coda pairs
#                 # Now we need to check compatibility
#                 # rules: consonants must be different mannars of articulation
#                 ending_coda = [None, None]
#                 for phoneme in phoneme_list:
#                     if phoneme == consonant_a or phoneme == consonant_b:
#                         if phoneme == consonant_a:
#                             ending_coda[0] = phoneme
#                         if phoneme == consonant_b:
#                             ending_coda[1] = phoneme
#                 if ending_coda[0].manner != ending_coda[1].manner:
#                     for vowel in vowel_list:
#                         count += 1
#                         print(f"{count}: {vowel + ending_coda[0].IPA + ending_coda[1].IPA}")

# title("Single Oneset and Dual Coda") # for example, |eops
# invalid_coda = ['|', '||', 'B', 'r'] # clicks aren't valid at all, and trills must be mono-phonemic
# for consonant_a in consonant_list:
#     if not consonant_a in invalid_coda:
#         for consonant_b in consonant_list:
#             if not consonant_b in invalid_coda:
#                 # both consonants are valid ending coda pairs
#                 # Now we need to check compatibility
#                 # rules: consonants must be different mannars of articulation
#                 ending_coda = [None, None]
#                 for phoneme in phoneme_list:
#                     if phoneme == consonant_a or phoneme == consonant_b:
#                         if phoneme == consonant_a:
#                             ending_coda[0] = phoneme
#                         if phoneme == consonant_b:
#                             ending_coda[1] = phoneme
#                 if ending_coda[0].manner != ending_coda[1].manner:
#                     for vowel in vowel_list:
#                         for consonant_c in consonant_list:
#                             count += 1
#                             print(f"{count}: {consonant_c + vowel + ending_coda[0].IPA + ending_coda[1].IPA}")

print(num_single_onset_end)