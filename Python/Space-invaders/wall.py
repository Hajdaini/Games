class Wall:
    WALL_WIDTH = 40
    WALL_HEIGHT = 5
    CANVAS_WIDTH = 0
    CANVAS_HEIGHT = 0

    def __init__(self, canvas, color, posX, number):
        self.canvas = canvas
        Wall.CANVAS_WIDTH = int(self.canvas['width'])
        Wall.CANVAS_HEIGHT = int(self.canvas['height'])
        self.initial_number_walls = number
        CENTER = Wall.CANVAS_WIDTH // 2 - (Wall.WALL_WIDTH * number // 2) + Wall.WALL_WIDTH
        self.id = canvas.create_rectangle(0, 0,  Wall.WALL_WIDTH , Wall.WALL_HEIGHT, fill=color)
        self.canvas.move(self.id, posX * Wall.WALL_WIDTH + CENTER, Wall.CANVAS_HEIGHT/2 + 40)
        self.wallX0, self.wallY0, self.wallX1, self.wallY1 = canvas.coords(self.id)
        self.x = 1

    def draw(self):
        self.wallX0, self.wallY0, self.wallX1, self.wallY1 = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.x, 0)


if __name__ == '__main__':
    print('Please run main.py')