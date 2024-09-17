import os

os.system('cls')

text = input("input text> ")

res = ''.join(format(ord(i), '08b') for i in text)

print(str(res))