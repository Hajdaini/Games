"""
@Author : AJDAINI Hatim
@Github : https://github.com/Hajdaini
"""

import random

class Pendu:
    def __init__(self, word, lg):
        self.word = word.upper()
        self.hide_word = list(len(self.word) * '-')
        self.current_try = 10
        self.lg = lg

    def check_charactere(self, cara):
        wordL = list(self.word)
        is_finding_it = False
        for i,c in enumerate(wordL):
            if wordL[i] == cara:
                self.hide_word[i] = cara
                is_finding_it = True
        if not is_finding_it:
            self.current_try -= 1
            self.draw()

        return ('characters you have found : ' if self.lg == 'en' else 'les caractères que vous avez trouvé : ') + ''.join(self.hide_word)

    def is_wining(self):
        return ''.join(self.hide_word).count('-') == 0

    def is_alive(self):
        return self.current_try > 0

    def get_score(self):
        return self.current_try * 100

    def draw(self):
        if self.lg == 'en' and self.current_try > 1:
            try_text = 'tries'
        elif self.lg == 'en' and self.current_try <= 1:
            try_text = 'try'
        elif self.lg == 'fr' and self.current_try <= 1:
            try_text = 'essai'
        else:
            try_text = 'essais'

        print(r"""
               ,==========Y===
           ||  /      |
           || /       |
           ||/        O  {} {} !
           ||        /|\
           ||        /|
           ||
          /||                                
         //||_________________________                         
            """.format(self.current_try, try_text))

    def get_random_word(cls, lg):
        with open('words/words_' + lg + '.txt', 'r') as file:
            return random.choice(file.read().splitlines())

    get_random_word = classmethod(get_random_word)

if __name__ == '__main__':
    print("il faut executer le fichier 'main.py' | you have to execute the file'main.py'")
