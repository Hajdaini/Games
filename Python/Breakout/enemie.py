class Enemie:
    ENEMIE_WIDTH = 30
    ENEMIE_HEIGHT = 5
    CANVAS_WIDTH = 0
    CANVAS_HEIGHT = 0

    def __init__(self, canvas, color, posX, posY, number):
        self.canvas = canvas
        Enemie.CANVAS_WIDTH = int(self.canvas['width'])
        Enemie.CANVAS_HEIGHT = int(self.canvas['height'])
        self.initial_number_enemies = number
        if number == 1:
            CENTER = Enemie.CANVAS_WIDTH // 2  - Enemie.ENEMIE_WIDTH // 2
        else:
            CENTER = Enemie.CANVAS_WIDTH // 2 - (Enemie.ENEMIE_WIDTH * number // 2) + Enemie.ENEMIE_WIDTH // 2
        self.id = canvas.create_rectangle(0, 0,  Enemie.ENEMIE_WIDTH , Enemie.ENEMIE_HEIGHT, fill=color)
        self.canvas.move(self.id, posX * Enemie.ENEMIE_WIDTH + CENTER, posY * Enemie.ENEMIE_HEIGHT)
        self.enemieX0, self.enemieY0, self.enemieX1, self.enemieY1 = canvas.coords(self.id)
        self.x = 1

    def draw(self):
        self.enemieX0, self.enemieY0, self.enemieX1, self.enemieY1 = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.x, 0)


if __name__ == '__main__':
    print('Please run main.py')