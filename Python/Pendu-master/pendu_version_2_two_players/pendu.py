import random
import time


class Pendu:
    def __init__(self):
        self.global_TRIES = 5
        self.current_try = 10
        self.score_player_1 = 0
        self.score_player_2 = 0
        self.best_score = 0
        self.lg = ""
        self.player_name_1 = ""
        self.player_name_2 = ""
        self.player_name_winner = ""
        self.category = ""
        self.difficulty = 1
        self.config_handle()
        self.word = self.get_random_word()
        self.hide_word = self.hide_the_word()
        self.player_1_turn = True
        self.find_word_directly = False

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

    def proposition_handle(self):
        proposition_check = input('You want to enter the word directly (1 for YES | 2 or other for NO) : ' if self.lg == 'en' else 'Vous voulez entrer le mot directement (1 pour OUI | 2 ou autre pour NON) : ')
        if proposition_check == "1":
            propositional_word = input("Enter the entire word :").upper()
            listed_word = list(self.word)
            if propositional_word == self.word:
                self.find_word_directly = True
                for i in range(len(self.hide_word)):
                    self.hide_word[i] = listed_word[i]

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
        else:
            self.proposition_handle()
        return ('characters : ' if self.lg == 'en' else 'Caractère restant : ') + ''.join(self.hide_word)

    def is_wining(self):
        if self.player_1_turn:
            self.score_player_1 += self.current_try * 100 * self.difficulty
        else:
            self.score_player_2 += self.current_try * 100 * self.difficulty
        return ''.join(self.hide_word).count('-') == 0

    def get_score(self):
        return self.best_score

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
        self.set_best_score()
        with open('score.txt', 'a') as file:
            file.write("\n[{}] SCORE de {} : {}".format(time.strftime("%Y-%m-%d %H:%I:%S"), self.player_name_winner, self.get_score()))

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
        self.category = category

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

    def player_name_choice(self, player_number):
        while True:
            player_name_choice = input(
                ('Choose a name player {} (without space) : '.format(player_number) if self.lg == 'en' else 'Veuillez entrer votre nom joueur {} (sans espace) : '.format(player_number)))
            if " " in player_name_choice:
                print("\n" + (
                    'Plz choose a name without space, retry again !' if self.lg == 'en' else 'Veuillez choisir un nom sans espace, resseayer encore !'))
            else:
                print("Bienvenue " + player_name_choice)
                break
        if player_number == 1:
            self.player_name_1 = player_name_choice
        elif player_number == 2:
            self.player_name_2 = player_name_choice

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
        for x in range(1,3):
            self.player_name_choice(x)

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
                if self.player_1_turn:
                    cara = input(('\nEnter your charactere Player 1 (-1 to exit) : ' if self.lg == 'en' else '\nEnter votre caractere Joueur 1 (-1 pour quitter): '))
                else:
                    cara = input(('\nEnter your charactere Player 2 (-1 to exit) : ' if self.lg == 'en' else '\nEnter votre caractere Joueur 2 (-1 pour quitter): '))
                if cara == '-1':
                    exit(0)
                print(self.check_charactere(cara.upper()))
                if self.find_word_directly:
                    self.find_word_directly = False
                    break
                self.player_1_turn = not self.player_1_turn  # changement de tour de joueur
            self.retry()
        self.congratulation_handle()

    def retry(self):
        self.reconfigure()
        self.global_TRIES -= 1
        print("\nBRAVO !!\n" + ("You only have" + str(
            self.global_TRIES) + " word to find, you can do it !\n" if self.lg == 'en' else "Il ne vous reste que " + str(
            self.global_TRIES) + " mot à trouver, vous pouvez le faire !\n"))
        print("Score de "+ self.player_name_1 + " : " + str(self.score_player_1))
        print("Score de "+ self.player_name_2 + " : " + str(self.score_player_2))
        print(self.word)
        self.get_difficulty()
        print(('New hidden word : ' if self.lg == 'en' else 'Nouveau mot caché : ') + ''.join(self.hide_word))

    def set_best_score(self):
        if self.score_player_1 > self.score_player_2:
            self.best_score = self.score_player_1
            self.player_name_winner = self.player_name_1
        else :
            self.best_score = self.score_player_2
            self.player_name_winner = self.player_name_2

    def loosing_handle(self):
        self.save_score()
        self.print_best_score()
        print(("\n" +
                  "you lose :'( the winner is the player {} with a score {} ".format(self.player_name_winner, self.best_score) if self.lg == 'en' else "Vous avez perdu :'( le gagnant est le joueur {} avec un score de {} ".format(self.player_name_winner, self.best_score)))
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
        print("\n" + ("The winner is the player {} with a score {} ".format(self.player_name_winner,
                                                                    self.best_score) if self.lg == 'en' else "Le gagnant est le joueur {} avec un score de {} ".format(
                self.player_name_winner, self.best_score)))


if __name__ == '__main__':
    p = Pendu()
    p.play()
