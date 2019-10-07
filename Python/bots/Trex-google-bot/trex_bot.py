from PIL import ImageGrab
import pyautogui
import time
import numpy

start_time = time.time()
distance_x_to_jump = 21
delta_time_jump = 0.04
step = 1


class Positions:
    play_button = (400, 374)
    dinosaur = (245, 397)


def startGame():
    pyautogui.click(Positions.play_button)
    print("Starting the game")
    pyautogui.keyDown('down')


def delta_time():
    global start_time
    return time.time() - start_time


def print_step():
    global step
    print("STEP " + str(step))
    step += 1


def jump():
    global delta_time_jump
    global start_time
    print("Jump at {0:.4f}s".format(delta_time()))
    pyautogui.keyUp('down')
    pyautogui.keyDown('space')
    time.sleep(delta_time_jump)
    pyautogui.keyUp('space')
    pyautogui.keyDown('down')


def sumOfPixels():
    global distance_x_to_jump
    box = (Positions.dinosaur[0], Positions.dinosaur[1], Positions.dinosaur[0] + distance_x_to_jump,
           Positions.dinosaur[1] + 10)
    image = ImageGrab.grab(box).convert('L')
    sum = numpy.array(image.getcolors()).sum()
    return sum


def playStep(dist_x, sum_of_pixels, time_next_step, time_jump=0):
    global delta_time_jump
    global distance_x_to_jump
    delta_time_jump = time_jump
    distance_x_to_jump = dist_x
    while True:
        if delta_time() < time_next_step:
            if sumOfPixels() != sum_of_pixels:
                jump()
        else:
            print_step()
            break


startGame()

print_step()
playStep(distance_x_to_jump, 457, 20, delta_time_jump)  # Step 1
playStep(27, 517, 30, 0.04)  # Step 2
playStep(39, 637, 40, 0.03)  # Step 3
playStep(44, 687, 48, 0.01)  # Step 4
playStep(50, 747, 58)  # Step 5
playStep(65, 897, 68)  # Step 6
playStep(75, 997, 78)  # Step 7
playStep(95, 1197, 88)  # Step 8

while True: # Step 9
    distance_x_to_jump = 118
    if sumOfPixels() != 1427:
        jump()