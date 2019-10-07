import random
import time


class Pendu:
    def __init__(self):

        self.global_TRIES = 5
        self.current_try = 10
        self.score = 0
        self.lg = ""
        self.player_name = ""
        self.category = ""
        self.difficulty = 1
        self.config_handle()
        self.word = self.get_random_word()
        self.hide_word = self.hide_the_word()

    def hide_the_word(self):
        word_listed = list(self.word)
        len_word = len(word_listed)
        if self.difficulty == 1 :
            for i in range(1,len_word - 1):
                if word_listed[i] != " ":
                    word_listed[i] = "-"
        elif self.difficulty == 2:
            self.current_try = 8
            for i in range(1, len_word):
                if word_listed[i] != " ":
                    word_listed[i] = "-"
        elif self.difficulty == 3:
            for i in range(len_word):
                self.current_try = 6
                if word_listed[i] != " ":
                    word_listed[i] = "-"
        return word_listed

    def reconfigure(self):
        self.word = self.get_random_word()
        self.current_try = 10
        self.hide_word = self.hide_the_word()

    def get_difficulty(self):
        len_word = len(self.word)
        if len_word < 5:
            difficulty = 1
        elif len_word >= 5 and len_word < 8:
            difficulty = 2
        else:
            difficulty = 3
        if self.difficulty == 1:
            level = ('easy' if self.lg == 'en' else 'facil')
        elif self.difficulty == 2:
            level = ('normal' if self.lg == 'en' else 'moyen')
        elif self.difficulty == 3:
            level = ('hard' if self.lg == 'en' else 'difficile')
        print(('Difficulty :' if self.lg == 'en' else 'dificulté : ') + str(difficulty) + " | " + ('Level :' if self.lg == 'en' else 'Niveau : ') + level)

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
        self.score += self.current_try * 100 * self.difficulty
        return ''.join(self.hide_word).count('-') == 0

    def get_score(self):
        return self.score

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

    def get_random_word(self):
            with open('words/' + self.category + '.txt', 'r') as file:
                return random.choice(file.read().splitlines()).upper()

    def save_score(self):
        with open('score.txt', 'a') as file:
            file.write("\n[{}] SCORE de {} : {}".format(time.strftime("%Y-%m-%d %H:%I:%S"), self.player_name, self.get_score()))

    def print_best_score(self):
        print('\nLIST OF BEST SCORES : ' if self.lg == 'en' else 'LISTE DES MEILLEURS SCORES : ')
        with open('score.txt', 'r') as file:
            top_score_limit = 10
            lines = file.read().splitlines()
            scores = []
            for line in lines:
                scores.append({"name": line.split(" ")[4], "score": int(line.split(" ")[6])})
            sorted_scores = sorted(scores, key=lambda k: k['score'], reverse=True)

            for index in range(top_score_limit):
                try:
                    print("Top {} : {} score {}".format(str(index + 1), sorted_scores[index]["name"],
                                                        sorted_scores[index]["score"]))
                except:  # ici si on essais d'affichier le top 5 alors que j'ai juste 1 joueur alors on aura l'exectiption our of range
                    break

    def category_choice(self):
        while True:
            category_choice = int(input((
                                            'Choose a category (1 => movie | 2 => singer | 3 => music) : ' if self.lg == 'en' else 'choisissez une catégorie (1 => film | 2 => chanteur | 3 => musique) : ')))
            if category_choice == 1:
                category = 'movie'
                print('Your category choise is movie' if self.lg == 'en' else 'Votre choix de catégorie est film')
                break
            elif category_choice == 2:
                category = "singer"
                print('Your category choise is singer' if self.lg == 'en' else 'Votre choix de catégorie est chanteur')
                break
            elif category_choice == 3:
                category = "music"
                print('Your category choise is music' if self.lg == 'en' else 'Votre choix de catégorie est musique')
                break
            else:
                print('\n' + ('Bad choice please retry' if self.lg == 'en' else 'Choix incorrecte, veuillez ressayer !'))
        self.category =  category

    def difficulty_choice(self):
        while True:
            difficulty_choice = int(input((
                                            'Choose a difficulty (1 => easy | 2 => normal | 3 => hard) : ' if self.lg == 'en' else 'choisissez une difficulté (1 => facil | 2 => moyen | 3 => compliqué) : ')))
            if difficulty_choice >= 1 and difficulty_choice <= 3:
                print('Your difficulty choise is ' if self.lg == 'en' else 'Votre choix de difficulté est ' + str(difficulty_choice))
                break
            else:
                print('\n' + ('Bad choice please retry' if self.lg == 'en' else 'Choix incorrecte, veuillez ressayer !'))
        self.difficulty = difficulty_choice

    def player_name_choice(self):
        while True:
            player_name_choice = input(
                ('Choose a name (without space) : ' if self.lg == 'en' else 'Choisissez un nom (sans espace) : '))
            if " " in player_name_choice:
                print("\n" + (
                    'Plz choose a name without space, retry again !' if self.lg == 'en' else 'Veuillez choisir un nom sans espace, resseayer encore !'))
            else:
                print("Bienvenue " + self.player_name)
                break
        self.player_name = player_name_choice

    def langage_choice(self):
        while True:
            lg = input("Entrer 'fr' pour le français | Enter 'en' for english : ").lower()
            if lg == 'fr' or lg == 'en':
                break
            else:
                print("\nil faut taper 'fr' ou 'en' | you have to type 'fr' or 'en'")
        self.lg = lg
        self.intro()

    def config_handle(self):
        self.langage_choice()
        self.category_choice()
        self.difficulty_choice()
        self.player_name_choice()

    def intro(self):
        print('\n')
        print((' WELCOME TO PENDU GAME ' if self.lg == 'en' else ' BIENVENUE AU JEU PENDU ').center(71, '*'))
        print((
                  ' FIND THE WORD CACHE 5 TIMES SUCCESSIVELY BY ENTERING THE CHARACTERS ' if self.lg == 'en' else ' TROUVEZ LE MOT CACHE 5 FOIS SUCCESSIVEMENT EN ENTRANT LES CARACTÈRES ').center(
            50))
        print(''.center(71, '*'))
        print("\n")
    
    def play(self):
        print(self.word)
        print('\n' + ('hidden word : ' if self.lg == 'en' else 'mot caché : ') + ''.join(self.hide_word))
        while self.global_TRIES > 0:
            while not self.is_wining():
                if self.current_try <= 0:
                    self.loosing_handle()
                    exit(0)
                cara = input(('\nEnter your charactere (-1 to exit) : ' if self.lg == 'en' else '\nEnter votre caractere (-1 pour quitter): '))
                if cara == '-1':
                    exit(0)
                print(self.check_charactere(cara.upper()))
            self.retry()
        self.congratulation_handle()

    def retry(self):
        self.reconfigure()
        self.global_TRIES -= 1
        print("\nBRAVO !!\n" + ("You only have" + str(
            self.global_TRIES) + " word to find, you can do it !\n" if self.lg == 'en' else "Il ne vous reste que " + str(
            self.global_TRIES) + " mot à trouver, vous pouvez le faire !\n"))
        print("Score : " + str(self.get_score()))
        print(self.word)
        self.get_difficulty()
        print(('New hidden word : ' if self.lg == 'en' else 'Nouveau mot caché : ') + ''.join(self.hide_word))

    def loosing_handle(self):
        self.save_score()
        self.print_best_score()
        print((
                  "you lose :'( your final score is " if self.lg == 'en' else "tu as perdu :'( votre score final est ") + str(
            self.get_score()))
        print(("The word was " if self.lg == 'en' else "le mot était ") + ''.join(self.word))


    def congratulation_handle(self):
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
        self.save_score()
        print(('YOU WIN' if self.lg == 'en' else 'VOUS AVEZ GAGNE'))
        self.print_best_score()
        print(('Your score is : ' if self.lg == 'en' else 'Votre scrore final est de : ') + str(self.get_score()))


if __name__ == '__main__':
    p = Pendu()
    p.play()
