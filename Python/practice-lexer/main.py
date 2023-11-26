import os

running = True
os.system('cls')
while running:
    user_input = input("tree script>")
    print(user_input)
    if user_input == "exit":
        running = False