import os

from jisho_api.word import Word

os.system('cls')

user_word = input("Please input the word that you want translated>")
r = Word.request(user_word)

print(r)
