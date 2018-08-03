import global_var


class Projectile:
    LARGE = 7
    CANVAS_WIDTH = 0
    CANVAS_HEIGHT = 0

    def __init__(self, canvas, color, player, player_projectiles, *other_pos):
        self.canvas = canvas
        self.player = player
        self.color = color
        self.player_projectiles = player_projectiles
        Projectile.CANVAS_WIDTH = int(self.canvas['width'])
        Projectile.CANVAS_HEIGHT = int(self.canvas['height'])
        self.id = self.canvas.create_oval(0,0, Projectile.LARGE, Projectile.LARGE, fill=color)
        if player_projectiles:
            self.canvas.move(self.id, self.player.playerX0 + self.player.player_width//2 - Projectile.LARGE//2, self.player.playerY0 - Projectile.LARGE)
        else:
            self.canvas.move(self.id, other_pos[0] - Projectile.LARGE // 2, other_pos[1])
        self.projectileX0, self.projectileY0, self.projectileX1, self.projectileY1 = (0, 0, 0, 0)
        self.speedY = 2.8
        if self.player_projectiles:
            self.y = -1
        else:
            self.y = 1

    def draw(self):
        self.canvas.move(self.id, 0, self.y * self.speedY)
        self.projectileX0, self.projectileY0, self.projectileX1, self.projectileY1 = self.canvas.coords(self.id)
        if self.projectileY0 <= 0:
            self.destroy_projectile()
        elif self.projectileY1 >= Projectile.CANVAS_HEIGHT:
            self.destroy_projectile()
        self.hit()

    def hit(self):
        if self.player_projectiles == False and self.projectileX1 >= self.player.playerX0 and self.projectileX0 <= self.player.playerX1 and self.projectileY1 >= self.player.playerY0 and self.projectileY0 <= self.player.playerY1:
            self.canvas.itemconfig(global_var.level_text, text="YOU LOST !", fill="yellow")
            self.destroy_projectile()
            global_var.stop_game = True
        for w in global_var.walls:
            if self.projectileX1 >= w.wallX0 and self.projectileX0 <= w.wallX1 and self.projectileY1 >= w.wallY0 and self.projectileY0 <= w.wallY1:
                self.destroy_projectile()
                return True
        for en in global_var.enemies:
            if self.player_projectiles == True and self.projectileX1 >= en.enemieX0 and self.projectileX0 <= en.enemieX1 and self.projectileY1 >= en.enemieY0 and self.projectileY0 <= en.enemieY1:
                self.destroy_projectile()
                self.destroy_enemie(en)
                if len(global_var.enemies) == 12:
                    global_var.level += 1
                    self.canvas.itemconfig(global_var.level_text, text='Level {}'.format(global_var.level))
                if len(global_var.enemies) == 0:
                    self.canvas.itemconfig(global_var.level_text, text="Congratulation YOU WIN !", fill="yellow")
                    global_var.stop_game = True
                return True
        return False

    def destroy_projectile(self):
        self.canvas.delete(self.id)
        global_var.projectiles.remove(self)

    def destroy_enemie(self, en):
        self.canvas.delete(en.id)
        global_var.enemies.remove(en)


if __name__ == '__main__':
    print('Please run main.py')
