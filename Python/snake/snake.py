import random, curses


# Config Variables
WIDTH, HEIGHT = 40, 25
INITIAL_BODY_SIZE = 8

## Init Variables
screenH, screenW = 0, 0
dirX, dirY = 0, 0
foodX, foodY = 0, 0
score = 0
snake = []
screen = curses.initscr()
key = curses.KEY_RIGHT
dead, pause = False, False


def cursesConfig():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, -1)  # Separator
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_YELLOW, - 1)
    curses.init_pair(7, curses.COLOR_MAGENTA, - 1)

    curses.curs_set(False)  # Remove the cursor from the terminal
    screenH, screenW = screen.getmaxyx()  # Get window size
    if screenW < WIDTH or screenH < (HEIGHT + 6):
        print("Please expand the size of your window")
        quit()


def drawArena():
    for x in range(WIDTH + 1):
        for y in range(HEIGHT + 1):
            if y == 0:
                if x != 0 and x != WIDTH:
                    window.addstr(y, x, "_", curses.A_BOLD)
            elif y == HEIGHT:
                if x != 0 and x != WIDTH:
                    window.addstr(y, x, "_", curses.A_BOLD)
            elif x == 0:
                window.addstr(y, x, "|", curses.A_BOLD)
            elif x == WIDTH:
                if y == HEIGHT:
                    window.addstr(y, x, "|", curses.A_BOLD)
                else:
                    window.addstr(y, x, "|", curses.A_BOLD)
            else:
                window.addstr(y, x, " ", curses.A_BOLD)
            window.addstr(HEIGHT, WIDTH, "|", curses.A_BOLD)
            window.addstr(HEIGHT, 0, "|", curses.A_BOLD)


def endGame(msg):
    curses.endwin()
    print(msg)
    exit()


def restartGame():
    global score, snake, key, dirX, dirY
    drawArena()
    score = 0
    snake = []
    initBody()
    key = curses.KEY_RIGHT
    dirX, dirY = 1, 0
    drawScore()
    drawFood()
    drawSnakeBody()


def initBody():
    for p in range(INITIAL_BODY_SIZE):
        snake.append([int(0.3 * WIDTH) + p, int(0.3 * HEIGHT)])


def drawSnakeBody():
    global snake
    for p in range(len(snake)):
        if p == len(snake) - 1:
            window.addstr(snake[p][1], snake[p][0],
                          'O', curses.color_pair(2))
        else:
            window.addstr(snake[p][1], snake[p][0],
                          '*', curses.color_pair(2))


def drawScore():
    global score
    window.addstr(HEIGHT + 2, 0, " Score {} ".format(score),
                  curses.color_pair(6))
    window.addstr(HEIGHT + 4, 0, " r : restart ".format(score),
                  curses.color_pair(3))
    window.addstr(HEIGHT + 4, 12, "  ".format(score), curses.color_pair(4))
    window.addstr(HEIGHT + 4, 14, " p : pause ".format(score),
                  curses.color_pair(3))
    window.addstr(
        HEIGHT + 6, 0, " Ctrl + c : quit the game ".format(score), curses.color_pair(3))


def drawFood():
    global foodX, foodY
    foodX = random.randint(2, WIDTH - 5)
    foodY = random.randint(2, HEIGHT - 5)
    window.addstr(foodY, foodX, "*", curses.color_pair(1))


def expandSnake():
    global score, snake
    drawFood()
    score += 10
    drawScore()
    snake.insert(0, [snake[0][0], snake[0][1]])


def handleKeyboard():
    global dirX, dirY, key, dead, pause
    next_key = window.getch()
    key = key if next_key == -1 else next_key

    if key == curses.KEY_DOWN and dirY != -1:
        dirX = 0
        dirY = 1
    if key == curses.KEY_UP and dirY != 1:
        dirX = 0
        dirY = -1
    if key == curses.KEY_LEFT and dirX != 1:
        dirX = -1
        dirY = 0
    if key == curses.KEY_RIGHT and dirX != -1:
        dirX = 1
        dirY = 0
    if key == ord('r'):
        if not pause:
            restartGame()
            dead = False
            pause = False
    if key == ord('p'):
        if not dead:
            drawArena()
            window.addstr(HEIGHT//2, WIDTH//2 - 3,
                          " PAUSE ", curses.color_pair(7))
            window.addstr(HEIGHT//2 + 1, WIDTH//2 - 10,
                          " Press c to continue ", curses.color_pair(7))
        pause = True
    if key == ord('c'):
        if not dead:
            drawArena()
            window.addstr(foodY, foodX, "*", curses.color_pair(1))
        pause = False


def arenaCollision():
    global snake
    if snake[head][0] >= WIDTH:
        window.addstr(snake[head][1], snake[head][0], '|', curses.A_BOLD)
        snake[head][0] = 1
    if snake[head][0] <= 0:
            window.addstr(snake[head][1], snake[head]
                          [0], '|', curses.A_BOLD)
            snake[head][0] = WIDTH - 1
    if snake[head][1] >= HEIGHT:
        window.addstr(snake[head][1], snake[head][0], '_', curses.A_BOLD)
        snake[head][1] = 1
    if snake[head][1] <= 0:
        window.addstr(snake[head][1], snake[head][0], '_', curses.A_BOLD)
        snake[head][1] = HEIGHT - 1


def reorganizeSnakeBodyPosition(head):
    global snake
    for p in range(head):
        window.addstr(snake[p][1], snake[p][0], ' ', curses.color_pair(2))
        snake[p][0] = snake[p + 1][0]
        snake[p][1] = snake[p + 1][1]
    snake[head][0] += dirX
    snake[head][1] += dirY


def checkDeath(head):
    global snake, dead
    for p in range(head):
        if (snake[head] == snake[p]):
            window.addstr(HEIGHT//2, WIDTH//2 - 5,
                          " GAME OVER ", curses.color_pair(5))
            window.addstr(HEIGHT//2 + 1, WIDTH//2 - 9,
                          " Press r to retry ", curses.color_pair(5))
            dead = True

cursesConfig()

try:
    window = curses.newwin(screenH, screenW, 0, 0)  # creates a new window
    window.keypad(True)
    window.timeout(75)
    drawArena()
    initBody()
    drawSnakeBody()
    drawScore()
    drawFood()


    while True:
        try:
            handleKeyboard()
            if not dead and not pause:
                head = len(snake) - 1
                if (snake[head][0] == foodX and snake[head][1] == foodY):
                    expandSnake()
                    head = len(snake) - 1 # the size of the snake has grown so we redefine the head
                arenaCollision()
                reorganizeSnakeBodyPosition(head)
                drawSnakeBody()
                checkDeath(head)
        except KeyboardInterrupt as e:
            endGame("Your score " + str(score))
except curses.error as e:
    endGame("Your window is too small" + str(score))
        
