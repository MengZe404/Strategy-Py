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
        Available arguments: me, Nusta, Lozar'''
        if player.lower() == '(me)':
            print(myStatus)
        elif player.lower() == '(nusta)':
            print(nustaStatus)
        elif player.lower() == '(lozar)':
            print(lozarStatus)
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
        self.inventory_list = ['(piece of gold)', '(small package)']

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
        global myStatus
        global nustaStatus
        global lozarStatus

        my_inventory = {
            '(piece of gold)': 0,
            '(small package)': 0
        }

######## Default Resources of the player are inversly proportional to the difficulty
        myStatus = {
            'gold': int(1000/self.difficulty_index),
            'soldier': int(5000/self.difficulty_index),
            'turn': 0,
            'victory': 0
        }

######### Default Resources of the opponents are directly proportional to the difficulty
        nustaStatus = {
            'gold': int(1000*self.difficulty_index),
            'soldier': int(5000*self.difficulty_index)
        }

        lozarStatus = {
            'gold': int(1000*self.difficulty_index),
            'soldier': int(4000*self.difficulty_index)
        }

#### Events
    def event(self):
        global event
        # Do not trigger the encounter_Oppo event before 30 moves
        if myStatus['turn'] <= 30:
            event_index = str(random.randint(1, len(event[0])))
        else:
            event_index = str(random.randint(1, len(event[0])))
        event_message = event[0][event_index]
        print("\n<Event> " + event_message)
        if event_index == '1':
            my_inventory.update({'(piece of gold)': int(my_inventory['(piece of gold)']) + 1 })
        elif event_index == '2':
            myStatus['gold'] -= 150
        elif event_index == '3':
            myStatus['soldier'] += 100
        elif event_index == '4':
            my_inventory.update({'(small package)': int(my_inventory['(small package)']) + 1 })
        elif event_index == '5':
            solve = input('\nWould you like to solve it? (yes/no): ')
            if solve.lower() == 'yes':
                self.puzzle_solving()
            else:
                print("\nYou found it boring and throw it away.")
        if event_index == '6':
            self.encounter_Oppo('lozar')
        if event_index == '7':
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
            myStatus['gold'] += gained_Resources
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

#### Boss fighting :)
    def encounter_Oppo(self, opponent):
        decision = input("\nWould you like to attack the opponent's kingdom? (yes / no): ").lower()
        if decision == "yes":
            if opponent == "lozar":
                self.opponent_index = 6
                if myStatus["gold"] >= lozarStatus["gold"] and myStatus["soldier"] >= lozarStatus["soldier"]:
                    self.attack(opponent)
                else:
                    print("\n<System> You do not have enough resources to attack.")
            if opponent == "nusta":
                self.opponent_index = 7
                if myStatus["gold"] >= nustaStatus["gold"] and myStatus["soldier"] >= nustaStatus["soldier"]:
                    pass
                else:
                    print("\n<System> You do not have the ability to attack.")
        else:
            print("\n<System> You run away before your opponent notice you.")
        
    def attack(self, opponent):
        lower_boundary = 1
        upper_boundary = 100
        bomb = random.randint(lower_boundary, upper_boundary)
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
                print("\n<System> BOMB! You lost the battle!\nYou lost 1000 golds and 2000 soldiers!")
                myStatus['gold'] -= 1000
                myStatus['soldier'] -= 2000
                break

            time.sleep(2)

            oppo_guess = random.randint(lower_boundary, upper_boundary)
            print('\n<' + opponent + '> Guess: ' + str(oppo_guess))
            if oppo_guess > bomb:
                print("\n<System> The guess is larger than bomb!")
                upper_boundary = oppo_guess
            elif oppo_guess < bomb:
                print("\n<System> The guess is smaller than bomb!")
                lower_boundary = oppo_guess
            else:
                print("\n<System> BOMB!\n\nCongratulations you have eliminate " + opponent + '!\nYou gained 1000 golds and 2000 soldiers from this victory')
                myStatus['gold'] += 1000
                myStatus['soldier'] += 2000
                myStatus['victory'] += 1
                break
        if myStatus['victory'] == 2:
            global victory_message
            print(victory_message)
            time.sleep(10)
            exit()

#### Actions
    def action_Use(self, item):
        if item in self.inventory_list:
            gained_Resources = random.randint(50,200) * int(my_inventory[item])
            myStatus['gold'] += gained_Resources
            print("\n<System> Used " + item + " - You have gained " + str(gained_Resources) + " gold!")
            my_inventory.update({item : 0})
        else:
            print('\n<System> Error: Invalid item')

    def action_Rest(self):
        myStatus['gold'] -= random.randint(1,50)
        myStatus['soldier'] += random.randint(1, 100)
        myStatus['turn'] += 1
    
    def action_Move(self):
        myStatus['turn'] += 1
        self.event()
        
# Execute the game
def runGame():
    game()
    game().initialise()
    commands().cmdloop()

if __name__ == '__main__':
    runGame()
    