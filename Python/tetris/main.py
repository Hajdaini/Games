import random
import curses
import time

# Config Variables
ROWS, COLUMNS = 20, 10


## Init Variables
screen = curses.initscr()
key = curses.KEY_DOWN
pause = False
screenH, screenW = 0, 0
initposition = (0, 0)  # (COLUMNS//2 - 1, 0)
posX, posY = initposition
moveLR = 0
counter = time.time()
deltaTime = 0.5
deltaTimeMoveDown = 0.03 / 2
arena = [[[0, 1] for _ in range(COLUMNS)]
         for _ in range(ROWS)]  # Store state and color
collisionLeftRight = "none"
score = 0
pieces = [
    [
        [1],
        [1],
        [1],
        [1]
    ],
    [
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [1, 0],
        [1, 0],
        [1, 1]
    ],

    [
        [0, 1],
        [0, 1],
        [1, 1]
    ],

    [
        [1, 0],
        [1, 0],
        [1, 1]
    ],

    [
        [0, 1],
        [1, 1],
        [1, 0]
    ],

    [
        [1, 0],
        [1, 1],
        [0, 1]
    ],

    [
        [1, 1],
        [1, 1]
    ]
]
pieces_copy = pieces.copy()
pieceNbr = random.randrange(len(pieces))
randomColor = random.randint(2, 7)
nextPieceNbr = random.randrange(len(pieces))
nextRandomColor = random.randint(2, 7)


def cursesConfig():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, -1, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_BLUE, -1)
    curses.init_pair(6, curses.COLOR_CYAN, -1)
    curses.init_pair(7, curses.COLOR_MAGENTA, -1)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_YELLOW, -1)
    curses.init_pair(10, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.curs_set(False)  # Remove the cursor from the terminal
    screenH, screenW = screen.getmaxyx()  # Get window size
    if screenW < COLUMNS or screenH < (ROWS):
        print("Please expand the size of your window")
        quit()


def endGame(msg):
    curses.endwin()
    print(msg)
    exit()

# For test only
# for r in range(ROWS):
#     for c in range(COLUMNS):
#         if c > 1 and r > ROWS - 3:
#             arena[r][c][0] = 1
      

def isGameOver():
    for c in range(COLUMNS):
        hit = 0
        for r in range(ROWS):
            if arena[r][c][0] == 1:
                hit += 1
                if hit >= ROWS:
                    return True
    return False


def drawArena():
    global score
    for r in range(ROWS):
        fillBoxNbr = 0
        for c in range(COLUMNS):
            if arena[r][c][0] == 1:
                fillBoxNbr += 1
                window.addstr(r, c, "■", curses.color_pair(arena[r][c][1]))
                if fillBoxNbr == COLUMNS:
                    arena.remove(arena[r])
                    arena.insert(0, [[0, 1] for _ in range(COLUMNS)])
                    score += 100
            else:
                window.addstr(r, c, "□", curses.color_pair(0))
    for c in range(COLUMNS + 2):
        window.addstr(ROWS, c, "■")
    for r in range(ROWS):
        window.addstr(r, COLUMNS + 1, " ", curses.color_pair(8))


def drawPiece(pieceNbr):
    for l in range(len(pieces[pieceNbr])):
        for c in range(len(pieces[pieceNbr][l])):
            if pieces[pieceNbr][l][c] != 0:
                window.addstr(l + posY, c + posX, "■", curses.color_pair(randomColor))


def storeBlock():
    global posY, posX, pieceNbr, moveLR, pieces, randomColor, nextPieceNbr, nextRandomColor
    moveLR = 0
    for l in range(len(pieces[pieceNbr])):
        for c in range(len(pieces[pieceNbr][l])):
            if pieces[pieceNbr][l][c] != 0:
                arena[l + posY][c + posX][0] = 1
                arena[l + posY][c + posX][1] = randomColor
    pieceNbr = nextPieceNbr
    randomColor = nextRandomColor
    nextPieceNbr = random.randrange(len(pieces))
    nextRandomColor = random.randint(2, 7)
    pieces = pieces_copy.copy()
    posX, posY = initposition


def collisionWithBorder():
    global collisionLeftRight
    collisionLeftRight = "none"
    for l in range(len(pieces[pieceNbr])):
        for c in range(len(pieces[pieceNbr][l])):
            if pieces[pieceNbr][l][c] == 1 and l + posY >= ROWS - 1:
                storeBlock()
                return
            if pieces[pieceNbr][l][c] == 1 and c + posX >= COLUMNS - 1:
                collisionLeftRight = "collisionRight"
            if pieces[pieceNbr][l][c] == 1 and c + posX <= 0:
                collisionLeftRight = "collisionLeft"


def collisionWithPieces():
    global collisionLeftRight
    for l in range(len(pieces[pieceNbr])):
        for c in range(len(pieces[pieceNbr][l])):
            if c + posX > 0 and pieces[pieceNbr][l][c] == 1 and arena[l + posY][c + posX - 1][0] == 1:
                collisionLeftRight = "collisionLeft"
            if c + posX < COLUMNS - 1 and  pieces[pieceNbr][l][c] == 1 and arena[l + posY][c + posX + 1][0] == 1:
                collisionLeftRight = "collisionRight"
            if (pieces[pieceNbr][l][c] == 1 and arena[l + posY + 1][c + posX][0] == 1):
                storeBlock()
                return


def rotate():
    global pieces, posX
    reverse_piece = pieces[pieceNbr][::-1]  # Reverse the list
    rotateBlock = list(list(elem) for elem in zip(*reverse_piece))  # Tranpose the list
    for l in range(len(rotateBlock)):
        for c in range(len(rotateBlock[l])):
            if rotateBlock[l][c] == 1 and c + posX >= COLUMNS:
                posX -= (c + posX - COLUMNS + 1)  # Shift the piece
    pieces[pieceNbr] = rotateBlock


def drawInfo():
    w, h = 8, 8
    frameY = 7
    window.addstr(ROWS - 5, COLUMNS + 6, " p : pause ", curses.color_pair(8))
    window.addstr(1, COLUMNS + 6, "Score {}".format(score), curses.color_pair(9))
    window.addstr(4, COLUMNS + 6, "Next Piece ")
    for x in range(w):
        for y in range(h):
            if y == 0 or y == h - 1:
                window.addstr(y + frameY - 2, COLUMNS + 6 + x, "■")
            elif x == 0 or x == w - 1:
                window.addstr(y + frameY - 2, COLUMNS + 6 + x, " ", curses.color_pair(8))
            else:
                window.addstr(y + frameY - 2, COLUMNS + 6 + x, " ")
    for l in range(len(pieces_copy[nextPieceNbr])):
        for c in range(len(pieces_copy[nextPieceNbr][l])):
            if pieces_copy[nextPieceNbr][l][c] != 0:
                window.addstr(l + frameY, COLUMNS + 9 + c, "■", curses.color_pair(nextRandomColor))


def handleKeyboard():
    global key, pause, moveLR, posY, counter
    key = window.getch()
    moveLR = 0
    if key != -1:
        if key == curses.KEY_DOWN:
             if time.time() > counter:
                counter = time.time() + deltaTimeMoveDown
                posY += 1
        if key == curses.KEY_UP:
            rotate()
        if key == curses.KEY_LEFT and collisionLeftRight != "collisionLeft":
            moveLR = -1
        if key == curses.KEY_RIGHT and collisionLeftRight != "collisionRight":
            moveLR = 1
        if key == ord('p'):
            drawArena()
            window.addstr(ROWS//2, COLUMNS//2 - 3, " PAUSE ", curses.color_pair(10))
            pause = not pause

try:
    cursesConfig()
    window = curses.newwin(screenH, screenW, 0, 0)  # creates a new window
    window.keypad(True)
    window.timeout(60)
    drawArena()
    drawPiece(pieceNbr)

    while True:
        try:
            if isGameOver():
                endGame("Game Over")
            collisionWithBorder()
            collisionWithPieces()
            handleKeyboard()
            if not pause:
                posX += moveLR
                if time.time() > counter:
                    counter = time.time() + deltaTime
                    posY += 1
                drawArena()
                drawInfo()
                drawPiece(pieceNbr)
        except KeyboardInterrupt as e:
            endGame("Bye, your score is {}".format(score))
except curses.error as e:
    endGame("Your window is too small")
