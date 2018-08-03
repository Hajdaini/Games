import global_var


class Ball:
    LARGE = 10
    CANVAS_WIDTH = 0
    CANVAS_HEIGHT = 0

    def __init__(self, canvas, color, player, enemies):
        self.canvas = canvas
        Ball.CANVAS_WIDTH = int(self.canvas['width'])
        Ball.CANVAS_HEIGHT = int(self.canvas['height'])
        self.player = player
        self.enemies = enemies
        self.id = self.canvas.create_oval(0, 0, Ball.LARGE, Ball.LARGE, fill=color)
        self.canvas.move(self.id, Ball.CANVAS_WIDTH / 2 - (Ball.LARGE // 2), Ball.CANVAS_HEIGHT / 2 - (Ball.LARGE // 2))
        self.ballX0, self.ballY0, self.ballX1, self.ballY1 = (0, 0, 0, 0)
        self.speedX = 3
        self.speedY = 2.8
        self.x = 1
        self.y = -1

    def draw(self):
        self.canvas.move(self.id, self.x * self.speedX, self.y * self.speedY)
        self.ballX0, self.ballY0, self.ballX1, self.ballY1 = self.canvas.coords(self.id)
        if self.ballX0 <= 0:
            self.x = 1
        elif self.ballX1 >= Ball.CANVAS_WIDTH:
            self.x = -1
        elif self.ballY0 <= 0:
            self.y = 1
        elif self.ballY1 >= Ball.CANVAS_HEIGHT:
            self.canvas.itemconfig(global_var.level_text, text="Oh no YOU LOOSE !", fill="red")
            global_var.stop_game = True
        elif self.hit():
            self.y = -1

    def hit(self):
        if self.ballX1 >= self.player.playerX0 and self.ballX0 <= self.player.playerX1 and self.ballY1 >= self.player.playerY0 and self.ballY0 <= self.player.playerY1:
            return True
        for en in self.enemies:
            if self.ballX1 >= en.enemieX0 and self.ballX0 <= en.enemieX1 and self.ballY1 >= en.enemieY0 and self.ballY0 <= en.enemieY1:
                self.destroy_enemie(en)
                if len(self.enemies) == 19:
                    global_var.level += 1
                    self.canvas.itemconfig(global_var.level_text, text='Level {}'.format(global_var.level))
                if len(self.enemies) == 10:
                    global_var.level += 1
                    self.canvas.itemconfig(global_var.level_text, text='Level {}'.format(global_var.level))
                if len(self.enemies) == 0:
                    self.canvas.itemconfig(global_var.level_text, text="Congratulation YOU WIN !", fill="yellow")
                    global_var.stop_game = True
                return True
        return False

    def destroy_enemie(self, en):
        self.canvas.delete(en.id)
        self.enemies.remove(en)


if __name__ == '__main__':
    print('Please run main.py')
