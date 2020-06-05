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
############################

print('''
 $$$$$$$$   $$$$$$$$$$ $$$$$$$$$      $$$     $$$$$$$$$$  $$$$$$$$$$    $$$$$$    $$      $$             ########    ##      ##
$$      $$      $$     $$      $$    $$ $$        $$      $$          $$$    $$$   $$    $$              ##     ##    ##    ## 
$$              $$     $$      $$   $$   $$       $$      $$          $$            $$  $$               ##  &   ##    ##  ##
 $$$$$$$$       $$     $$$$$$$$$    $$   $$       $$      $$$$$$$$$$  $$  $$$$$$     $$$$      =====     ##     ##      ####
        $$      $$     $$   $$     $$=====$$      $$      $$          $$      $$      $$                 #######         ##
 $$     $$      $$     $$    $$    $$     $$      $$      $$          $$$    $$$      $$                 ##              ##
 $$$$$$$$$      $$     $$     $$   $$     $$      $$      $$$$$$$$$$    $$$$$$$       $$                 ##              ##
==================================================================================================================================
''')


# Create data.json
json_format = {
    "message":[]
}

open('data.json', 'a').close()

# Get data
with open('data.json', 'r+') as database:
    try:
        game_assets = json.load(database)
    except:
        json.dump(json_format, game_assets, indent=4)
    message = game_assets['message']


# Print welcome message and game tutorial
welcome_message = message[0]['welcome_message']
game_play = message[0]['game_play']
secret_message = message[0]['secret_message']

print(welcome_message)
print(game_play)


# Commands (functions) that can be executed by the user
class commands(cmd.Cmd):
    intro = '\n##########################################################################################################\n\n#Game Begins\nType ? or help to list all available commands'
    name = input("What's your name: ")
    prompt = '\n<' + name + '> '

#### System
    def do_exit(self, arg):
        'exit(): exit the game'
        exit()

    def do_restart(self, arg):
        'restart(): restart the game'
        confirm = input('\nAre you sure you want to restart the game? This will clear all your progress! (yes / no): ').lower()
        if confirm == 'yes':
            print('\nGame Restarted')
            game().initialise()
        else:
            pass
    
    def do_shell(self, s):
        '''
        shell(arg): execute shell commands

        Available arguments: clear, ls, cat
        '''
        os.system(s)
        
    
##### Properties
    def do_status(self, player):
        '''
        status(arg): check the status (resources & populations & statistics) of a specific kingdom

        Available arguments: me, Nusta, Lozar
        '''
        if player.lower() == '(me)':
            print(myStatus)
        elif player.lower() == '(nusta)':
            print(nustaStatus)
        elif player.lower() == '(lozar)':
            print(lozarStatus)
        else:
            print('Error: Invalid argument')


    def do_inventory(self, arg):
        'inventory(): display all the owned items'
        print(my_inventory)
    
    def do_decode(self, code):
        '''
        decode(arg): gain a special award if you can find the correct passcode
        
        Hint: the passcode can be found easily somewhere in this folder! :)
        '''
        if code == '(show me the gift, please!)':
            print(secret_message)
    
##### Actions
    def do_use(self, item):
        'use(arg): use an item'
        if item != ():
            try:
                game().action_Use(item)
            except:
                print('Error: Invalid item')
        else:
            print('Error: use() takes 1 argument but 0 is given')

    def do_rest(self, item):
        'rest(): do not move for this round'
        game().action_Rest()



# The actual game
class game:
    def __init__(self):
        self.move = 0
        self.statistics = []
        self.inventory_list = ['(some gold)']

    # The amount of resources issued to the player and opponents, calculated based on the difficulty of the game
    def initialise(self):
        mode = ''
        while mode == '':
            mode = input('Select a mode (easy, hard, insane): ').lower()
            if mode == 'easy':
                difficulty_index = 1
            elif mode == 'hard':
                difficulty_index = 2
            elif mode == 'insane':
                difficulty_index = 4
            else:
                print('\nError: your mode selection is invalid.')
                mode = ''

        # Default values
        global my_inventory
        global myStatus
        global nustaStatus
        global lozarStatus

        my_inventory = {
            '(some gold)': 1
        }

        myStatus = {
        'golds': int(1000/difficulty_index),
        'soldiers': int(5000/difficulty_index)
        }

        nustaStatus = {
            'golds': int(1000*difficulty_index),
            'soldiers': int(5000*difficulty_index)
        }

        lozarStatus = {
            'golds': int(100*difficulty_index),
            'soldiers': int(4000*difficulty_index)
        }

    def action_Use(self, item):
        for item in self.inventory_list:
            myStatus['golds'] += random.randint(50, 100) * int(my_inventory[item])
            my_inventory.pop(item)

    def action_Rest(self):
        self.move += 1
        myStatus['golds'] -= random.randint(1,50)
        myStatus['soldiers'] += random.randint(1, 100)
        

def runGame():
    game()
    game().initialise()
    commands().cmdloop()

if __name__ == '__main__':
    runGame()