import random
print("Rock, Paper, Scissors!")
while True:
    user_input = input(">").lower()
    computer_choice = random.choice(["rock", "paper", "scissors"])
    print(f"computer: {computer_choice}")
    match user_input:
        case "rock":
            match computer_choice:
                case "paper":
                    print("Lose")
                case "scissors":
                    print("Win")
        case "paper":
            match computer_choice:
                case "rock":
                    print("Win")
                case "scissors":
                    print("Lose")
        case "scissors":
            match computer_choice:
                case "rock":
                    print("Lose")
                case "paper":
                    print("Win")
    if user_input == computer_choice:
        print("Draw")