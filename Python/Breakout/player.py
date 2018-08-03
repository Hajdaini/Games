class Player:
    PLAYER_WIDTH = 100
    PLAYER_HEIGHT = 5
    CANVAS_WIDTH = 0
    CANVAS_HEIGHT = 0

    def __init__(self, canvas, color):
        self.canvas = canvas
        Player.CANVAS_WIDTH = int(self.canvas['width'])
        Player.CANVAS_HEIGHT = int(self.canvas['height'])
        self.id = self.canvas.create_rectangle(0, 0, Player.PLAYER_WIDTH, Player.PLAYER_HEIGHT, fill=color)
        self.canvas.move(self.id, Player.CANVAS_WIDTH / 2 - (Player.PLAYER_WIDTH // 2), Player.CANVAS_HEIGHT - Player.PLAYER_HEIGHT)
        self.playerX0, self.playerY0, self.playerX1, self.playerY1 = (0,0,0,0)
        self.speedX = 5
        self.x = 0
        self.binds()

    def binds(self):
        self.canvas.bind_all('<Left>', self.turnLeft)
        self.canvas.bind_all('<Right>', self.turnRight)
        self.canvas.bind_all('<KeyRelease>', self.release)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        self.playerX0, self.playerY0, self.playerX1, self.playerY1 = self.canvas.coords(self.id)
        if self.playerX0 < 0 or self.playerX1 > Player.CANVAS_WIDTH:
            self.x = 0

    def turnLeft(self, event):
        self.playerX0, self.playerY0, self.playerX1, self.playerY1 = self.canvas.coords(self.id)
        if self.playerX0 >= 0:
            self.x = -self.speedX
        else:
            self.x = 0

    def turnRight(self, event):
        self.playerX0, self.playerY0, self.playerX1, self.playerY1 = self.canvas.coords(self.id)
        if self.playerX1 <= Player.CANVAS_WIDTH:
            self.x = self.speedX
        else:
            self.x = 0

    def release(self, event):
        self.x = 0

if __name__ == '__main__':
    print('Please run main.py')
