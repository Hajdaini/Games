# coding: utf-8
"""
@Author : AJDAINI Hatim
@GitHub : https://github.com/Hajdaini
"""

from pendu import Pendu

def intro(lg):
    print('\n')
    print((' WELCOME TO PENDU GAME ' if lg == 'en' else ' BIENVENUE AU JEU PENDU ').center(50, '*'))
    print((' FIND THE WORD BY ENTERING CARACTERES ' if lg == 'en' else ' TROUVEZ LE MOT EN ENTRANT LES CARACTÈRES ').center(50))
    print(''.center(50, '*'))

def langage_handle():
    while True:
        lg = input("Entrer 'fr' pour le français | Enter 'en' for english : ").lower()
        if lg == 'fr' or lg == 'en':
            break
        else:
            print("il faut taper 'fr' ou 'en' | you have to type 'fr' or 'en'")
    return lg

if __name__ == '__main__':

    lg = langage_handle()
    intro(lg)
    p = Pendu(Pendu.get_random_word(lg), lg)

    print('\n' + ('hidden word : ' if lg == 'en' else 'mot caché : ') + ''.join(p.hide_word))

    while not p.is_wining():
        if not p.is_alive():
            print(("you lose :'(" if lg == 'en' else "tu as perdu :'("))
            exit(0)
        cara = input(('\nEnter your charactere (-1 to exit) : ' if lg == 'en' else '\nEnter votre caractere (-1 pour quitter): '))
        if cara == '-1':
            exit(0)
        print(p.check_charactere(cara.upper()))

    print(r"""
     ___________
    '._==_==_=_.'
    .-\:      /-.
   | (|:.     |) |
    '-|:.     |-'
      \::.    /
       '::. .'
         ) (
       _.' '._
      `"""""""`
    """)
    print(('YOU WIN' if lg == 'en' else 'VOUS AVEZ GAGNE'))
    print(('Your score is : ' if lg == 'en' else 'Votre scrore est de : ') + str(p.get_score()))
