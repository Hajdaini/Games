"""
@Author : AJDAINI Hatim
@GitHub : https://github.com/Hajdaini
"""

from tkinter import *
from projectile import Projectile
from player import Player
from enemie import Enemie
from wall import Wall
import global_var
import time, random


def draw_enemies():
    number_enemies_variable = 36  # PLEASE DONT CHANGE IT
    for y in range(0, 15, 3):
        global enemies
        for x in range(0, number_enemies_variable, 4):
            enemie = Enemie(canvas, 'green', x, y, number_enemies_variable)
            global_var.enemies.append(enemie)
        number_enemies_variable -= 8
        if number_enemies_variable <= 0:
            number_enemies_variable = 1


def begin_play(canvas):
    global_var.stop_game = False
    global_var.play_button.place_forget()
    canvas.pack()


def on_closing():
    window.destroy()


def window_position(window):
    screen_width = int(window.winfo_screenwidth())
    screen_height = int(window.winfo_screenheight())
    window_width = global_var.WIDTH
    window_height = global_var.HEIGHT
    window_x = (screen_width // 2) - (window_width // 2)
    window_y = (screen_height // 2) - (window_height // 2)
    return '{}x{}+{}+{}'.format(window_width, window_height, window_x, window_y)


def draw_walls():
    number_walls_variable = 15  # PLEASE DONT CHANGE IT
    for x in range(0, number_walls_variable, 3):
        global_var.walls.append(Wall(canvas, 'brown', x, number_walls_variable))


def enemies_fire():
    for e in global_var.enemies:
        if len(global_var.enemies) > 10:
            if random.randint(0, 100) % 2 == 0:
                global_var.projectiles.append(Projectile(canvas, 'red', player, False, e.enemieX0 + e.enemie_width // 2, e.enemieY1))
        else :
            global_var.projectiles.append(Projectile(canvas, 'red', player, False, e.enemieX0 + e.enemie_width // 2, e.enemieY1))


# Window configuration
window = Tk()
window.configure(background='black')
window.title('AJDAINI Space invaders')
window.resizable(False, False)
window.geometry(window_position(window))
window.protocol("WM_DELETE_WINDOW", on_closing)

# Window Widgets
label = Label(window, text="Welcome to my second GitHub tkinter game\nCreated by AJDAINI Hatim", bg='black', fg='#DC4C46', font='Arial 16 italic')
guide_label = Label(window, text="→ : Move Right\n← : Move Left\nMouse Click : Fire", bg='gray20', fg='white', font='Arial 14', width=20, height=4)
global_var.play_button = Button(window, text='PLAY', font='Arial 12 normal', bg='#DC4C46', fg='white', command=lambda: begin_play(canvas))
label.place(relx=0.5, rely=0.7, anchor=CENTER)
guide_label.place(relx=0.5, rely=0.5, anchor=CENTER)
global_var.play_button.place(relx=0.5, rely=0.3, anchor=CENTER)

# Canvas configuration
canvas = Canvas(window, width=global_var.WIDTH, height=global_var.HEIGHT, bg='black', bd=0, highlightthickness=0)
global_var.level_text = canvas.create_text(global_var.WIDTH//2, global_var.HEIGHT//2, text='Level {}'.format(global_var.level), fill="gray20", font=('Arial', 20, 'italic'))
guide_text = canvas.create_text(global_var.WIDTH//2, global_var.HEIGHT - 100, text='→ : Move Right\n← : Move Left\nMouse Click : Fire'.format(global_var.level), fill="gray20", font=('Arial', 16))
player = Player(canvas, 'white')
draw_enemies()
draw_walls()


if __name__ == '__main__':
    timer = time.time() + 1
    while True:
        #try except because when windows is destroyed the draws functions are still running
        try:
            if time.time() > timer:
                enemies_fire()
                timer = time.time() + 1
            if not global_var.stop_game :
                if global_var.level == 1:
                    for en in global_var.enemies:
                        if en.enemieX0 <= 0:
                            for en2 in global_var.enemies:
                                en2.x = 1
                        elif en.enemieX1 >= global_var.WIDTH:
                            for en2 in global_var.enemies:
                                en2.x = -1
                        en.draw()

                if global_var.level == 2:
                    for en in global_var.enemies:
                        if en.enemieX0 <= 0:
                            en.x = 1
                        elif en.enemieX1 >= global_var.WIDTH:
                            en.x = -1
                        en.draw()

                for b in global_var.projectiles:
                    try:
                        b.draw()
                    except:
                        print('die')
                player.draw()
            window.update_idletasks()# make the animation smooth
            window.update()
            time.sleep(0.01)
        except:
            print('Good bye')
            break
