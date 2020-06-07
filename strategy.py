'''
Strategy-Py, version 1.0

A text based RTS game!

(C) MengZe 2020-present
'''

# Copyright information.
__author__ = 'MengZe'
__copyright__ = '(C) MengZe 2020-present'
__license__ = 'Public Domain'
__version__ = '1.0.0'

# Libraries
############################
import cmd
import os
import json
import random
import time
############################

print('''
 $$$$$$$$   $$$$$$$$$$ $$$$$$$$$      $$$     $$$$$$$$$$  $$$$$$$$$$    $$$$$$    $$      $$             ########    ##      ##
$$      $$      $$     $$      $$    $$ $$        $$      $$          $$$    $$$   $$    $$              ##     ##    ##    ## 
$$              $$     $$      $$   $$   $$       $$      $$          $$            $$  $$               ##  &   ##    ##  ##
 $$$$$$$$       $$     $$$$$$$$$    $$   $$       $$      $$$$$$$$$$  $$  $$$$$$     $$$$      =====     ##     ##      ####
        $$      $$     $$   $$     $$=====$$      $$      $$          $$      $$      $$                 #######         ##
$$      $$      $$     $$    $$    $$     $$      $$      $$          $$$    $$$      $$                 ##              ##
 $$$$$$$$$      $$     $$     $$   $$     $$      $$      $$$$$$$$$$    $$$$$$$       $$                 ##              ##
==================================================================================================================================
''')


# Create data.json
json_format = {
    "message":[]
}

open('assets.json', 'a').close()

# Get data
with open('assets.json', 'r+') as database:
    try:
        game_assets = json.load(database)
    except:
        json.dump(json_format, game_assets, indent=4)
    message = game_assets['message']
    event = game_assets['event']
    puzzle = game_assets['puzzle']

welcome_message = message[0]['welcome_message']
game_play = message[0]['game_play']
secret_message = message[0]['secret_message']
victory_message = message[0]['victory_message']

# Print welcome message and game tutorial
print(welcome_message)
print(game_play)


# Commands (functions) that can be executed by the user
class commands(cmd.Cmd):
    intro = '\n##########################################################################################################\n\n#Game Begins\n\nType ? or help to list all available commands'
    name = input("What's your name: ")
    prompt = '\n<' + name + '> '

#### System
    def do_exit(self, arg):
        '\nexit(): exit the game'
        exit()

    def do_restart(self, arg):
        '\nrestart(): restart the game'
        confirm = input('\n<System> Are you sure you want to restart the game? This will clear all your progress! (yes / no): ').lower()
        if confirm == 'yes':
            print('\n<System> Game Restarted!')
            game().initialise()
        else:
            pass
    
    def do_shell(self, s):
        '''
        shell(arg): execute shell commands.
        Available arguments: clear, ls, cat'''
        os.system(s)
        
    
##### Properties
    def do_status(self, player):
        '''
        status(arg): check the status (resources & populations & statistics) of a specific kingdom
        Available arguments: me, nusta, lozar, all'''
        if player.lower() == '(me)':
            print(my_status)
        elif player.lower() == '(nusta)':
            print(nusta_status)
        elif player.lower() == '(lozar)':
            print(lozar_status)
        elif player.lower() == '(all)':
            print("My: " + str(my_status))
            print("Lozar: " + str(lozar_status))
            print("Nusta: " + str(nusta_status))
        else:
            print('\n<System> Error: Invalid argument')

    def do_inventory(self, arg):
        '\ninventory(): display all the owned items'
        print(my_inventory)

    def do_decode(self, code):
        '''
        decode(arg): gain a special award if you can find the correct passcode
        Hint: the passcode can be found easily somewhere in this folder! :)'''
        if code == '(show me the gift, please!)':
            print(secret_message)
    
##### Actions
    def do_use(self, item):
        '\nuse(arg): use an item'
        if item != ():
            game().action_Use(item)
        else:
            print('\n<System> Error: use() takes 1 argument but 0 is given')

    def do_rest(self, item):
        '''
        rest(): do not move in this round
        Effect: decrease the amount of gold and increase the number of soldiers'''
        game().action_Rest()
    
    def do_move(self, arg):
        '''
        move(): move one step
        Effect: trigger special events'''
        game().action_Move()



# The actual game
class game:
    def __init__(self):
        self.inventory_list = ['(bag of gold)', '(mysterious package)', '(potion)']

##### The amount of resources issued to the player and opponents, calculated based on the difficulty of the game
    def initialise(self):
        mode = ''
        while mode == '':
            mode = input('\nSelect a mode (easy, hard, insane): ').lower()
            if mode == 'easy':
                self.difficulty_index = 1
            elif mode == 'hard':
                self.difficulty_index = 2
            elif mode == 'insane':
                self.difficulty_index = 4
            else:
                print('\n<System> Error: your mode selection is invalid.')
                mode = ''

######## Default values
        global my_inventory
        global my_status
        global nusta_status
        global lozar_status

        my_inventory = {
            '(bag of gold)': 0,
            '(mysterious package)': 0,
            '(potion)': 0
        }

######## Default Resources of the player are inversly proportional to the difficulty
        my_status = {
            'gold': int(1000/self.difficulty_index),
            'soldier': int(5000/self.difficulty_index),
            'HP': 100,
            'defend': 1,
            'turn': 0,
            'victory': 0
        }

######### Default Resources of the opponents are directly proportional to the difficulty
        nusta_status = {
            'gold': int(1000*self.difficulty_index),
            'soldier': int(5000*self.difficulty_index),
            'HP': 100,
            'defend': 1
        }

        lozar_status = {
            'gold': int(1000*self.difficulty_index),
            'soldier': int(4000*self.difficulty_index),
            'HP': 100,
            'defend': 1
        }

#### Events
    def event(self):
        global event
        # Do not trigger the encounter_Oppo event before 30 moves
        if my_status['turn'] <= 50:
            posibility = random.randint(1,10)
            if posibility >= 9:
                event_index = str(random.randint(1, len(event[0])-2))
            else:
                event_index = str(random.randint(1, len(event[0])-5))
        else:
            event_index = str(random.randint(1, len(event[0])))
        event_message = event[0][event_index]
        print("\n<Event> " + event_message)
        if event_index == '1':
            my_inventory.update({'(bag of gold)': int(my_inventory['(bag of gold)']) + 1 })
        elif event_index == '2':
            my_status['gold'] -= random.randint(1, 100)
        elif event_index == '3':
            my_status['soldier'] += random.randint(1,100)
        elif event_index == '4':
            my_inventory.update({'(mysterious package)': int(my_inventory['(mysterious package)']) + 1 })
        elif event_index == '5':
            solve = input('\nWould you like to solve it? (yes/no): ')
            if solve.lower() == 'yes':
                self.puzzle_solving()
            else:
                print("\nYou found it boring and throw it away.")
        elif event_index == '6':
            answer = input('\nWould you like to play with him? (yes/no): ').lower()
            if answer == 'yes':
                self.guessing_game()
            else:
                print('\nYou ignored him.')
        elif event_index == '7':
            answer = input('\nWould you like to find another way? (yes/no): ').lower
            if answer == 'yes':
                luck = random.randint(1,10)
                if luck < 7:
                    print("\n<System> You fall into the river. Next time don't take the risk! (lost 200 gold and 100 soldiers)")
                    my_status['gold'] -= 200
                    my_status['soldier'] -= 100
                if luck > 7:
                    print("\n<System> You safely passed through the river!")
            else:
                print("<System> You spent 30 minutes looking for another way and some of your soldiers run away due to the hot summer weather! (lost 100 soldiers)")
                my_status['soldier'] -= 100
        elif event_index == '8':
            answer = input('\nWould you like to send your soldiers to fight the fire? (yes/no): ').lower()
            if answer == 'yes':
                luck = random.randint(1, 10)
                if luck < 7:
                    print("\n<System> After 2 hours of fighting, the village is safe!\nYou lost 200 soldiers and the villagers thank you a lot and gave you 500 gold! (- 200 soldiers & + 500 gold)")
                    my_status['gold'] += 500
                    my_status['soldier'] -= 200
                else:
                    print("\n<System> After 2 hours of fighting, the village is safe!\nThe villagers thank you a lot and gave you 500 gold! (+ 500 gold)")
                    my_status['gold'] += 500
            else:
                print("\nYou run away with your soldiers and some of them are angry with you unresponsiveness! (-100 soldiers)")
                my_status['soldier'] -= 100

        elif event_index == '9':
            self.encounter_Oppo('lozar')
        elif event_index == '10':
            self.encounter_Oppo('nusta')

 #### Just for fun!       
    def puzzle_solving(self):
        global puzzle
        puzzle_index = str(random.randint(1, len(puzzle[0])))
        correct_message = "\n<System> Congrats! Your answer is correct"
        incorrect_message = "\nUnfortunately your answer is incorrect. Try again next time."
        print('\n<System> Puzzle: ' + puzzle[0][puzzle_index])
        puzzle_answer = input('\nWrite your answer here: ')
        def correct():
            print(correct_message)
            gained_Resources = random.randint(50,200)
            my_status['gold'] += gained_Resources
            print("\n<System> You have gained " + str(gained_Resources) + " gold!")
        if puzzle_index == '1':
            if puzzle_answer == '35':
                correct()
            else:
                print(incorrect_message)
        if puzzle_index == '2':
            if puzzle_answer == '81':
                correct()
            else:
                print(incorrect_message)
        if puzzle_index == '3':
            if puzzle_answer == '201':
                correct()
            else:
                print(incorrect_message)
        if puzzle_index == '4':
            if puzzle_answer == '48':
                correct()
            else:
                print(incorrect_message)
        if puzzle_index == '5':
            if puzzle_answer == '64':
                correct()
            else:
                print(incorrect_message)
        if puzzle_index == '6':
            if puzzle_answer == '6':
                correct()
            else:
                print(incorrect_message)
        if puzzle_index == '7':
            if puzzle_answer == '5040':
                correct()
            else:
                print(incorrect_message)
        if puzzle_index == '8':
            if puzzle_answer == '16':
                correct()
            else:
                print(incorrect_message)
        if puzzle_index == '9':
            if puzzle_answer == '165':
                correct()
            else:
                print(incorrect_message)

#### Special Events
    def guessing_game(self):
        lower_boundary = 1
        upper_boundary = 100
        bomb = random.randint(lower_boundary, upper_boundary)
        print("\n<Mysterious Man> Young man, here is the game rule: I have randomly placed a BOMB in the number range 1 to 100. Who guess the bomb correctly will be the loser.")
        while True:
            my_guess = int(input('\nGuess a number within ' + str(lower_boundary) + ' - ' + str(upper_boundary) + ' : '))
            if my_guess <= lower_boundary or my_guess >= upper_boundary:
                print("\n<System> Invalid Guess")
                continue
            elif my_guess > bomb:
                print("\n<System> The guess is larger than bomb!")
                upper_boundary = my_guess
            elif my_guess < bomb:
                print("\n<System> The guess is smaller than bomb!")
                lower_boundary = my_guess
            else:
                print("\n<System> BOMB! You lost the game")
                break

            time.sleep(2)

            oppo_guess = random.randint(lower_boundary+1, upper_boundary-1)
            print('\n<Mysterious Man> Guess: ' + str(oppo_guess))
            if oppo_guess > bomb:
                print("\n<System> The guess is larger than bomb!")
                upper_boundary = oppo_guess
            elif oppo_guess < bomb:
                print("\n<System> The guess is smaller than bomb!")
                lower_boundary = oppo_guess
            else:
                print("\n<System> BOMB!\n\nCongratulations YOU WON!\nYou gained 1000 golds and 2000 soldiers from this victory")
                my_status['gold'] += 1000
                my_status['soldier'] += 2000
                if my_inventory['(potion)'] == 0:
                    my_inventory.update({'(potion)' : 1})
                break

#### Boss fighting :)
    def encounter_Oppo(self, opponent):
        lozar_status['HP'] = 100
        lozar_status['defend'] = 1 
        nusta_status['HP'] = 100
        nusta_status['defend'] = 1
        my_status['HP'] = 100
        my_status['defend'] = 1
        decision = input("\nWould you like to attack the opponent's kingdom? The cost will be 1000 gold and 1000 soldiers (yes / no): ").lower()
        if decision == "yes":
            my_status['gold'] -= 1000
            my_status['soldier'] -= 1000
            if opponent == "lozar":
                if my_status["gold"] >= lozar_status["gold"] and my_status["soldier"] >= lozar_status["soldier"]:
                    self.fight('lozar')
                else:
                    print("\n<System> You do not have enough resources to attack.")
            if opponent == "nusta":
                if my_status["gold"] >= nusta_status["gold"] and my_status["soldier"] >= nusta_status["soldier"]:
                    self.fight('nusta')
                else:
                    print("\n<System> You do not have the ability to attack.")
        else:
            print("\n<System> You run away before your opponent notice you.")

#### Battle System       
    def fight(self, opponent):
        opponent_name = '\n<' + opponent + '> '
        print(opponent_name + "Nice to see you here, my good 'friend'. So, let's fight!")
        action = ['attack', 'defend']
        while True:
            if my_status['HP'] > 0:
                my_action = input("\n<System> You turn. What action would you take? (attack/defend): ").lower()
                if my_action == action[0]:
                    if opponent == 'lozar':
                        damage = int(random.randint(1, 20) / lozar_status['defend'])
                        lozar_status['HP'] -= damage
                        print("\n<System> " + opponent + ' lost ' + str(damage) + ' HP; he has ' + str(lozar_status['HP']) + ' left')
                    elif opponent == 'nusta':
                        damage = int(random.randint(1, 20) / nusta_status['defend'])
                        print("\n<System> " + opponent + ' lost ' + str(damage) + ' HP; he has ' + str(nusta_status['HP']) + ' left')
                        nusta_status['HP'] -= damage
                elif my_action == action[1]:
                    my_status['defend'] += 1
                else:
                    print('\n<System> Unknown action')
                    continue         
            else:
                print('\n<System> You lost the battle! (- 2000 gold, - 2000 soldiers')
                my_status['gold'] -= 2000
                my_status['soldier'] -= 2000
                break

            if lozar_status['HP'] <= 0 or nusta_status['HP'] <= 0:
                print('\n<System> You won the battle! (+ 2000 gold, + 2000 soldiers)')
                my_status['gold'] += 2000
                my_status['soldier'] += 2000
                my_status['victory'] += 1
                break

            time.sleep(2)

            opponent_action = action[random.randint(0,1)]
            print(opponent_name + opponent_action)
            if opponent_action == action[0]:
                damage = int(random.randint(1,40) / my_status['defend'])
                my_status['HP'] -= damage
                print("\n<System> You lost " + str(damage) + " HP; you have " + str(my_status['HP']) + ' left')
            elif opponent_action == action[1]:
                if opponent == 'lozar':
                    lozar_status['defend'] += 1
                elif opponent == 'nusta':
                    nusta_status['defend'] +=1
            
        if my_status['victory'] == 2:
            global victory_message
            print(victory_message)
            time.sleep(10)
            exit()

#### Actions
    def action_Use(self, item):
        if item in self.inventory_list:
            if item == '(potion)':
                if my_status['HP'] <= 30:
                    my_status['HP'] += 50
                    print("\n<System> Used potion and recovered 50% HP! Now your HP = " + str(my_status['HP']))
                    my_inventory.update({item : 0})
                else:
                    print("\n<System> Your HP is higher than 30%")
            else:
                gained_Resources = random.randint(50,200) * int(my_inventory[item])
                my_status['gold'] += gained_Resources
                print("\n<System> Used " + item + " - You have gained " + str(gained_Resources) + " gold!")
                my_inventory.update({item : 0})
        else:
            print('\n<System> Error: Invalid item')

    def action_Rest(self):
        my_status['gold'] -= random.randint(1,50)
        my_status['soldier'] += random.randint(1, 100)
        my_status['turn'] += 1
    
    def action_Move(self):
        my_status['turn'] += 1
        self.event()
        
# Execute the game
def runGame():
    game()
    game().initialise()
    commands().cmdloop()

if __name__ == '__main__':
    runGame()
    