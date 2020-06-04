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

welcome_message = '''

Welcome to Strategy-Py, a simple and fun RTS game made in Python!

# Background Story:

People, Society, Culture, Education, Economics... 
The world is having a difficult time due to the rapid war.

You, as the king of your kingdom, will bring peace to your people.
Use your power and resources to eliminate the other kingdoms and dominate this unpeaceful land!

##########################################################################################################

# Kingdoms:
Devs Empire (you)
Nusta Kingdom (opponent no.1)
Lozar Kingdom (opponent no.2)
'''

import cmd

print('''

 $$$$$$$$   $$$$$$$$$$ $$$$$$$$$      $$$     $$$$$$$$$$  $$$$$$$$$$    $$$$$$    $$      $$             ########    ##      ##
$$      $$      $$     $$      $$    $$ $$        $$      $$          $$$    $$$   $$    $$              ##     ##    ##    ## 
$$              $$     $$      $$   $$   $$       $$      $$          $$            $$  $$               ##  &   ##    ##  ##
 $$$$$$$$       $$     $$$$$$$$$    $$   $$       $$      $$$$$$$$$$  $$  $$$$$$     $$$$      =====     ##     ##      ####
        $$      $$     $$   $$     $$=====$$      $$      $$          $$      $$      $$                 #######         ##
 $$     $$      $$     $$    $$    $$     $$      $$      $$          $$$    $$$      $$                 ##              ##
 $$$$$$$$$      $$     $$     $$   $$     $$      $$      $$$$$$$$$$    $$$$$$$       $$                 ##              ##
=================================================================================================================================================

''')

# Commands (functions) that can be executed by the user
class commands(cmd.Cmd):
    intro = '\nType ? or help to list all available commands'
    name = input("What's your name: ")
    prompt = '\n<' + name + '> '

    def do_exit(self, arg):
        'exit(): exit the game'
        exit()
    
    def do_status(self, player):
        '''
        status(arg): check the status (resources & populations & statistics) of a specific kingdom

        Available arguments: me, Nusta, Lozar
        '''
        if player == '(me)':
            print(myStatus)
        elif player == '(Nusta)':
            print(nustaSatus)
        elif player == '(Lozar)':
            print(lozarSatus)
        else:
            print('Error: Invalid argument')

    def do_restart(self, arg):
        'restart(): restart the game'
        confirm = input('\nAre you sure you want to restart the game? This will clear all your progress! (yes / no): ')
        if confirm == 'yes':
            print('Game Restarted')
            game().initialise()
        else:
            pass

    def do_inventory(self, arg):
        'inventory(): display all the owned items'
        print(inventory)

    def do_use(self, item):
        'use(arg): use an item'
        if item:            
            game().use(item)
            # except:
            #     print('Error: Invalid item')
        else:
            print('Error: use() takes 1 argument but 0 is given')

    def do_stay(self, item):
        'stay(): do not move for this round'
        game().stayCost()

inventory = {}

class game:
    def __init__(self):
        self.inventory = inventory
        self.move = 0

    # The amount of resources issued to the player and opponents, calculated based on the difficulty of the game
    def initialise(self):
        mode = ''
        while mode == '':
            mode = input('\nSelect a mode (easy, hard, insane): ').lower()
            if mode == 'easy':
                difficulty_index = 1
            elif mode == 'hard':
                difficulty_index = 2
            elif mode == 'insane':
                difficulty_index = 4
            else:
                print('Error: your mode selection is invalid.\n')
                mode = ''
        
        myStatus = {
            'golds': 1000/difficulty_index,
            'soldiers': 5000/difficulty_index,
            'statistics': 'None'
        }

        nustaSatus = {
            'golds': 1000*difficulty_index,
            'soldiers': 5000*difficulty_index,
            'statistics': 'None'
        }

        lozarSatus = {
            'golds': 800*difficulty_index,
            'soldiers': 4000*difficulty_index,
            'statistics': 'None'
        }

    def use(self, item):
        self.inventory.pop(item)
    
    def stayCost(self):



           


def runGame():
    print(welcome_message)
    game()
    game().initialise()
    commands().cmdloop()

if __name__ == '__main__':
    runGame()