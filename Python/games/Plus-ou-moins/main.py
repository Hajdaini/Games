"""
@Author : AJDAINI Hatim
@GitHub : https://github.com/Hajdaini
"""

import random
from plusoumoins import PlusouMoins

def intro():
    print(''.center(50, '*') + '\n' + ' WELCOME TO AJDAINI PLUS OU MOINS'.center(50, '*') + '\n' + ''.center(50, '*'))
    print(r"""
                              _____                       
                      _____  |K  WW|                      
              _____  |Q  ww| |   {)|                      
       _____ |J  ww| |   {(| |(v)%%| _____                
      |10 v ||   {)| |(v)%%| | v%%%||A_ _ |               
      |v v v||(v)% | | v%%%| |_%%%>||( v )|               
      |v v v|| v % | |_%%%O|        | \ / |               
      |v v v||__%%[|                |  .  |               
      |___0I|                       |____V|               
    """)
    print(''.center(50, '*') + '\n' + ' TROUVE LE NOMBRE ENTRE 1 à 100 '.center(50, '*') + '\n' + ''.center(50, '*') + '\n')

if __name__ == '__main__':
    p = PlusouMoins(random.randint(1,100))
    intro()

    while True:
        print('Votre argent : ' + str(p.money) + ' euros')
        retry = input('Appuyer sur O  pour jouer ou autre pour quitter : ')
        if retry == 'O' or retry == 'o':
            p.reset_try
        else:
            exit(0)

        while True:
            if p.has_no_money():
                break
            while True:
                try:
                    mise = int(input('\nEntrer votre mise (-1 pour quitter) : '))
                    break
                except:
                    print('il faut rentrer un nombre !')
            p.check_if_can_exit(mise)
            if mise < -1:
                print('votre chiffre doit être positive ! (sauf -1 pour quitter)')
            elif int(mise) > p.money:
                print('votre mise est trop grande, vous ne poessedez que ' + str(p.money) + ' euros')
            else:
                print('Vous avez misé ' + str(mise) + ' euros')
                break

        while True :
            if p.check_tries(mise):
                break
            try:
                number_player = int(input('\nEntrer le chiffre masqué (-1 pour quitter) : '))
            except:
                print('Il faut rentrer un nombre !')
            if p.check_number(number_player, mise):
                break
