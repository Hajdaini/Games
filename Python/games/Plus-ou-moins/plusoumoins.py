"""
@Author : AJDAINI Hatim
@Github : https://github.com/Hajdaini
"""

TRY = 5
DEFAUT_MONEY = 200

class PlusouMoins:
    def __init__(self, hidden_number):
        with open('money.txt', 'r') as file:
            self.money = int(file.readline())
        self.current_try = TRY
        self.hidden_number = hidden_number

    def check_tries(self, mise):
        if self.current_try <= 0:
            print('Perdu le numero était : ' + str(self.hidden_number))
            self.money -= mise
            with open('money.txt', 'w') as file:
                file.write(str(self.money))
            return True

    def check_number(self, number_player, mise):
        self.check_if_can_exit(mise, number_player)
        if self.hidden_number > number_player:
            self.current_try -= 1
            print('Il ne vous reste plus que ' + str(self.current_try) + (' chance' if self.current_try < 2 else ' chances'))
            print("C'est plus grand !\n")
            return False
        elif self.hidden_number < number_player:
            self.current_try -= 1
            print('Il ne vous reste plus que ' + str(self.current_try) +  (' chance' if self.current_try < 2 else ' chances'))
            print("C'est plus petit !\n")
            return False
        else:
            money_winned = self.current_try * mise * 2
            self.money += money_winned
            self.draw_trophee()
            print('bien jouer vous avez gagné ' + str(money_winned) +' euros !')
            with open('money.txt', 'w') as file:
                file.write(str(self.money))
            return True

    def has_no_money(self):
        if self.money <= 0:
            print('vous abez perdu !'  + '\n')
            with open('money.txt', 'r+') as file:
                if int(file.readline()) <= 0:
                    file.write(str(DEFAUT_MONEY))
            return True
        else:
            return  False

    def check_if_can_exit(self, mise = 1, number_player = 1):
        if number_player == -1 or mise == -1:
            print('Aurevoir !')
            exit(0)

    def reset_try(self):
        print('commençons !')
        self.current_try = TRY

    def draw_trophee(self):
        print(r"""
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

if __name__ == '__main__':
    print("il faut lancer le fichier 'main.py' !")
