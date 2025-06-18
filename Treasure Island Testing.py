print('''*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/______/_
*******************************************************************************''')

print("Welcome to Treasure Island! Survive and find the long lost treasure")

def crossroad():
    while True:
        direction = input("You find yourself awake in a forest. "
                          "The campfire has died out. You don't seem to remember where you are. "
                          "You find a path and walk towards it and come to a crossroad. "
                          "Do you want to go 'left' or 'right'? \n").lower()
        if direction == "left":
            return beach_path()
        elif direction == "right":
            return forest_path1()
        else:
            print("Invalid choice. Try again.")


def beach_path():
    while True:
        choice = input("You keep walking down the path until you reach a beach. "
                       "Nothing but water. You look at the distance and see a small island not too far. "
                       "Do you want to 'swim' to it or 'look for a boat'?\n").lower()
        if choice == "swim":
            print("You attempt to swim to the island. "
                  "Halfway though you notice sharks are circling you. "
                  "You tire out and cant stay up. The sharks come up and eat you. Game Over.")
            return "Game Over"
        elif choice == "look for a boat":
            return boat_path()
        else:
            print("Invalid choice. Try again.")


def forest_path1():
    while True:
        choice = input("You reach a wooded area. Nothing but trees surround you. "
                       "You hear noises within the forest. "
                       "Do you 'investigate' or 'go back' where you came?\n").lower()
        if choice == "investigate":
            return forest_path2()
        elif choice == "go back":
            return crossroad()
        else:
            print("Invalid choice. Try again.")


def forest_path2():
    while True:
        choice = input("You investigate the noise. "
                       "Turns out it was goblins looking for loot. "
                       "They see you eyeing them. They pull out their swords and chase you. "
                       "Do you 'run back' or 'pick up a weapon'?\n").lower()
        if choice == "pick up a weapon":
            return forest_path3()
        elif choice == "run back":
            print("You trip on a branch running away. The goblin catches up to you and kills you. Game Over")
            return "Game Over"
        else:
            print("Invalid choice. Try again.")


def forest_path3():
    while True:
        choice = input("Eventually you find yourself at a beach and a boat on the shore. "
                       "You see in the horizon a small island with a castle. "
                       "Do you 'take the boat', 'swim' to the island, or 'stay on land' and look around\n").lower()
        if choice == "take the boat":
            return boat_path2()
        elif choice == "swim to the island":
            print("You attempt to swim to the island. "
                  "Sharks circle and eat you. Game Over.")
            return "Game Over"
        elif choice == "stay on land":      #expand story
            print("You wait but nothing happens. The goblins find you again. Game Over.")
            return "Game Over"
        else:
            print("Invalid choice. Try again.")


def boat_path():
    while True:
        choice = input("You look around for a boat and eventually you find one not too far. "
                       "You pick up the oar and start rowing to the island. "
                       "Halfway through you notice sharks are circling you. "
                       "Do you 'hit them' with the oar or 'keep rowing'?\n").lower()
        if choice == "hit them":
            print("The sharks took offense you hit them and attack the boat. You capsize and they eat you. Game Over")
            return "Game Over"
        elif choice == "keep rowing":
            return island_path()
        else:
            print("Invalid choice. Try again.")


def boat_path2():
    while True:
        choice = input("You took the boat to the island. "
                       "Halfway through you notice sharks are circling you. "
                       "Do you 'hit them' with the oar or 'keep rowing'\n").lower()
        if choice == "hit them":
            print("The sharks took offense you hit them and attack the boat. You capsize and they eat you. Game Over")
            return "Game Over"
        elif choice == "keep rowing":
            return island_path()
        else:
            print("Invalid choice. Try again.")


def island_path():
    while True:



def play_again_prompt():
    while True:
        again = input("Do you want to play again? (y/n): ").lower()
        if again == "y":
            return True
        elif again == "n":
            print("Thanks for playing! Goodbye.")
            return False
        else:
            print("Please type 'y' for yes or 'n' for no.")


# Main Game Loop
while True:
    result = crossroad()

    if result == "Game Over":
        print("\n--- You died! ---\n")
    elif result == "Success":
        print("\n--- You survived the adventure! ---\n")

    if not play_again_prompt():
        break

