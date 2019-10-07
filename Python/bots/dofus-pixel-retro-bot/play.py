from PIL import Image
from pynput import keyboard
import pyscreenshot as ImageGrab
import os, time, random, pyautogui

ble = [ (235, 189, 5), (238, 195, 5), (233, 192, 14), (241, 195, 7), (235, 217, 30), (240, 194, 8), (249, 215, 46), (249, 222, 21), (230, 214, 53), (178, 128, 11), (181, 147, 40), (162, 102, 7), (233, 204, 45), (182, 126, 39) ]
orge = [(64, 162, 0), (87, 141, 5), (99, 144, 29), (91, 146, 5), (84, 180, 14), (75, 176, 0), (127, 149, 47), (107, 170, 25), (95, 127, 0), (108, 135, 1), (58, 131, 14), (71, 134, 0), (106, 195, 16)]
avoine = [(189, 125, 0), (214, 124, 0), (220, 161, 0), (216, 136, 0), (221, 168, 3), (183, 115, 0), (224, 162, 0), (251, 207, 0)]
houblon = [(37, 93, 54), (43, 94, 101), (9, 72, 78), (20, 89, 92), (29, 99, 54), (13, 97, 63), (32, 92, 90), (19, 87, 85), (45, 134, 37), (30, 125, 40), (88, 122, 59), (97, 137, 55), (59, 156, 64), (26, 100, 59)]
resources = [houblon]


map = open("play/maps/-24 - 42", 'r')

# x_pad, y_pad = 1, 193
x_pad, y_pad  = 294, 51
rest_pad_x, rest_pad_y = 1333, 775
keyinput = keyboard.Controller()
lastResourcePosX, lastResourcePosY = 0, 0
beginFight = False
path = os.path.dirname(os.path.abspath(__file__)) + "/play"


def randWait(min, max):
    time.sleep(round(random.uniform(min, max), 2))


def Focus(click=False):
    if click == False:
        pyautogui.moveTo(random.randint(25, 300), random.randint(200, 700))
    else:
        pyautogui.click(random.randint(25, 300), random.randint(200, 700))


def Screencap(save = False):
    box = (x_pad+1, y_pad+1, x_pad+rest_pad_x, y_pad+rest_pad_y)
    im = ImageGrab.grab(bbox=box)
    if save:
        im.save( os.path.join(path , 'screenshot.jpg'), "JPEG")
    return im


# Fonctionne que pour un écran 1920 x 1080 (le faire en pourcentage pour multi screen)
def ScreenCapChangeMap(direction):
    deltaX, deltaY = 1, 1
    if direction == "UP":
        box = (x_pad+deltaX, y_pad+deltaY, x_pad+rest_pad_x, y_pad+100)
    elif direction == "LEFT":
        box = (x_pad+deltaX, y_pad+deltaY, x_pad+120, y_pad+rest_pad_y)
    elif direction == "RIGHT":
        deltaX = 1213
        box = (x_pad+deltaX, y_pad+1 + deltaY,
               x_pad+rest_pad_x, y_pad+rest_pad_y)
    elif direction == "BOTTOM":
        deltaY = 685
        box = (x_pad+deltaX, y_pad+1 + deltaY,
               x_pad+rest_pad_x, y_pad+rest_pad_y)
    im = ImageGrab.grab(bbox=box)
    im.save(os.path.join(path, 'move/' + direction +'.jpg'), "JPEG")
    return deltaX, deltaY, im


def isInColor(im, color, successMax):
    findIt = False
    w, h = im.size
    success = 0
    x_pos, y_pos = 0, 0
    for i in range(w):
        for j in reversed(range(h)):
            r, g, b = im.getpixel((i, j))
            if (r, g, b) in color:
                success += 1
                x_pos, y_pos = i, j
                break
        if success >= successMax:
            findIt = True
            break
    return findIt, x_pos, y_pos, r, g, b

def isInFight():
    Focus()
    colorFight = [(35, 33, 214), (142, 138, 165), (0, 0, 255), (0, 0, 255), (153, 153, 153),
                  (153, 153, 153), (51, 51, 51), (153, 153, 153), (142, 134, 94), (255, 33, 33), (238, 132, 40)]
    imgFight = Screencap()
    imgFight.save(os.path.join(path, 'fight/detect-fight.jpg'), "JPEG")
    inFight = False
    findIt, x_pos, y_pos, r, g, b = isInColor(imgFight, colorFight, (len(colorFight) - 2))
    if findIt:
        inFight = True
        print("FIGHT ({}, {}) ({}, {}, {})".format(x_pos, y_pos, r, g, b))
    return inFight


def movePlayerInFight(enemy_posX, enemy_posY):
    # WIDTH = x_pad + enemy_posX
    # HEIGHT = y_pad + enemy_posY
    Focus(True)
    player_posX, player_posY = 0, 0
    colorPlayer = [(198, 67, 47), (220, 204, 204)]
    imgPlayerPos = Screencap()
    imgPlayerPos.save(os.path.join(path, 'fight-move.jpg'), "JPEG")

    findIt, player_posX, player_posY, r, g ,b = isInColor(imgPlayerPos, colorPlayer, 1)
    if findIt:
        pX, pY = player_posX + x_pad, player_posY + y_pad
        deltaX, deltaY = enemy_posX - pX, enemy_posY - pY
        if deltaX > 65:
            deltaX = 65
        if deltaX < - 65:
            deltaX = -65 
        if deltaY > 65:
            deltaY = 65
        if deltaY < - 65:
            deltaY = -65
        
        im = ImageGrab.grab()
        if im.getpixel((pX + deltaX, pY + deltaY)) in [(51, 51, 51), (153, 153, 153)]:
            print("OBSTACLE")
            deltaX= random.randint(-70, 70)
            deltaY= random.randint(-70, 70)
        print("FIGHT MOVE ({}, {}) ({}, {}, {})".format(player_posX, player_posY, r, g, b))
        randWait(0.2, 0.3)
        pyautogui.doubleClick(x=pX + deltaX, y=pY + deltaY)


def detectFight():
    global beginFight
    colorEnemy = [(32, 30, 218), (39, 38, 220), (16, 15, 236)]
    while True:
        if not isInFight():
            if beginFight:
                Focus(True)
                keyinput.press(keyboard.Key.esc)
                randWait(0.1, .15)
                keyinput.release(keyboard.Key.esc)
                beginFight = False
                print("END OF FIGHT")
            break
        else:
            beginFight = True
            Focus(True)
            imgFight = Screencap()
            imgFight.save(os.path.join(path, 'fight/attack.jpg'), "JPEG")
            findIt, x_pos, y_pos, r, g, b = isInColor(imgFight, colorEnemy, 1)

            if findIt:
                movePlayerInFight((x_pos + x_pad+x_pos), (y_pos + y_pad))
                randWait(1, 2)
                print("ATTACK ({}, {}) ({}, {}, {})".format(
                    x_pos, y_pos, r, g, b))
                keyinput.press("é")
                randWait(0.1, 0.15)
                pyautogui.click(x=x_pad+x_pos + 10, y=y_pad+y_pos)
                randWait(0.1, 0.15)
                keyinput.release("é")
                randWait(0.1, 0.15)
                keyinput.press("y")
                randWait(0.1, 0.15)
                keyinput.release("y")
                randWait(0.1, 0.15)
                Focus()
            randWait(8, 9)


def changeMap(direction):
    global keyinput
    Focus(True)
    keyinput.press("e")
    randWait(0.2, 0.25)
    colorChangeMapArrow = [(255, 0, 0), (206, 28, 16),
                           (255, 104, 40), (249, 15, 2)]
    colorChangeMapSquare = [(236, 245, 202), (239, 246, 212), (231, 242, 190), (239, 247, 212), (239, 232, 211), (239, 235, 209), (
        240, 234, 210), (238, 239, 219), (239, 236, 216), (179, 157, 67), (250, 249, 246), (250, 249, 246), (242, 239, 232), (235, 231, 208)]
    keyinput.press("a")
    keyinput.release("a")
    time.sleep(0.5)
    deltaX, deltaY, imgChangeMap = ScreenCapChangeMap(direction)
    imgChangeMap.save(os.path.join(path, 'move.jpg'), "JPEG")
    w, h = imgChangeMap.size
    x_pos, y_pos = 0, 0
    successSquare = 0
    successArrow = 0
    for i in range(w):
        for j in reversed(range(h)):
            r, g, b = imgChangeMap.getpixel((i, j))
            if direction != "BOTTOM":
                if (r, g, b) in colorChangeMapSquare:
                    successSquare += 1
                    x_pos, y_pos = i, j
            if (r, g, b) in colorChangeMapArrow:
                successArrow += 1
                x_pos, y_pos = i, j
        # priorité au arrow car + précis
        if successArrow >= 1:
            pyautogui.click(x=x_pad+x_pos + deltaX,
                            y=y_pad+y_pos + deltaY + 30)
            break
        if successSquare >= 1:
            pyautogui.click(x=x_pad+x_pos + deltaX + 30,
                            y=y_pad+y_pos + deltaY - 10)
            break
    print("MOVE " + direction + str((r, g, b)))
    keyinput.release("e")
    randWait(9.2, 9.5)


def jobClick(x, y):
    pyautogui.click(x=x_pad+x, y=y_pad+y)
    randWait(0.2, 0.25)
    pyautogui.click(x=x_pad+x+10, y=y_pad+y+45)
    randWait(0.1, 0.13)
    Focus()
    randWait(11.2, 11.4)


# work only in 1920 x 1080 resolution
def detectLevelUp():
    imLvlUp = ImageGrab.grab()
    colorLvlUp = [(255, 97, 0), (247, 93, 0), (255, 97, 0), (251, 95, 0)]
    posLvlUp = [(1037, 489), (1004, 491), (924, 488), (885, 490)]
    successLevelUp = 0
    for pos in posLvlUp:
        r, g, b = imLvlUp.getpixel(pos)
        if (r, g, b) in colorLvlUp:
            successLevelUp += 1
            randWait(0.1, 0.12)
    if successLevelUp >= len(posLvlUp):
        print("LEVEL UP")
        pyautogui.click(963, 491)
        Focus()


def detectResource():
    global lastResourcePosX, lastResourcePosY
    keyinput.press("e")
    randWait(0.2, 0.25)
    im = Screencap()
    w, h = im.size
    x_pos, y_pos = 0, 0
    n = 0
    isGetResource = False
    
    for i in range(w):
        for j in reversed(range(h)):
            r, g, b = im.getpixel((i, j))

            for resource in resources:
                if (r, g, b) in resource :
                    n += 1
                    x_pos, y_pos = i, j
                    print("JOB ({}, {}) ({}, {}, {})".format(x_pos, y_pos, r, g, b))
            if (n >= 3):
                if (lastResourcePosX, lastResourcePosY) == (x_pos, y_pos):
                    print("JOB (clicked already) ({}, {}) ({}, {}, {})".format(x_pos, y_pos, r, g, b))
                    n = 0
                    break
                isGetResource = True
                jobClick(x_pos, y_pos)
                lastResourcePosX, lastResourcePosY = x_pos, y_pos
                print("---------------")
    keyinput.release("e")
    return isGetResource


def __main__():
    try:
        Focus(True)
        time.sleep(0.2)
        while True:
            detectLevelUp()
            detectFight()
            if detectResource():
                continue
            direction = map.readline().replace("\n", "")
            if not direction or direction == "":
                    map.seek(0)
                    continue
            changeMap(direction)
    except KeyboardInterrupt:
        pass
    map.close()


__main__()