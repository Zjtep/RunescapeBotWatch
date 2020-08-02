import pyautogui
import RandTime
import random
import time
from time import sleep
from random import randint
import math

# from autopy.mouse import (
#     move, click, get_pos,
#     LEFT_BUTTON,
#     RIGHT_BUTTON,
#     CENTER_BUTTON
# )

def click():
    #autopy.mouse.click()
    # pyautogui.moveTo(100, 200)
    pyautogui.mouseDown(button='left')
    RandTime.randomTime(2, 7)
    # RandTime.randTime(0, 0, 0, 0, 0, 1)  # time between click
    pyautogui.mouseUp(button='left')

def right_click():
    #autopy.mouse.click()
    # pyautogui.moveTo(100, 200)
    pyautogui.mouseDown(button='right')
    RandTime.randomTime(2, 7)
    # RandTime.randTime(0, 0, 0, 0, 0, 1)  # time between click
    pyautogui.mouseUp(button='right')

def move_to_radius(coord):
    coord = list(coord)

    x = random.randint(coord[0]+6,coord[2]+coord[0]-6)
    y = random.randint(coord[1]+6,coord[3]+coord[1]-6)

    speed = 0.5
        # duration_of_move=duration
    # print x,y
    curr_x, curr_y = pyautogui.position()
    # calculates the distance from current position to target position
    distance = int(((x - curr_x) ** 2 + (y - curr_y) ** 2) ** speed)
    # calculates a random time to make the move take based on the distance
    duration_of_move = (distance * random.random() / 2000) + speed
    # move the mouse to our position and takes the time of our duration just
    # calculated
    pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeInOutQuad)

def click_radius(coord):
    coord = list(coord)

    x = random.randint(coord[0]+6,coord[2]+coord[0]-6)
    y = random.randint(coord[1]+6,coord[3]+coord[1]-6)

    speed = 0.5
        # duration_of_move=duration
    # print x,y
    curr_x, curr_y = pyautogui.position()
    # calculates the distance from current position to target position
    distance = int(((x - curr_x) ** 2 + (y - curr_y) ** 2) ** speed)
    # calculates a random time to make the move take based on the distance
    duration_of_move = (distance * random.random() / 2000) + speed
    # move the mouse to our position and takes the time of our duration just
    # calculated
    pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeInOutQuad)
    click()


def move_mouse_to_click(x, y):
    # takes current mouse location and stores it
    while(True):
        try:
            curr_x, curr_y = pyautogui.position()
            # calculates the distance from current position to target position
            distance = int(((x - curr_x)**2 + (y - curr_y)**2)**0.5)
            # calculates a random time to make the move take based on the distance
            duration_of_move = (distance * random.random() / 2000) + 0.5
            # move the mouse to our position and takes the time of our duration just
            # calculated
            pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeInOutQuad)
            click()
            #pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeOutElastic)
            break
        except:
            print('paused for 10 seconds')
            time.sleep(10)

def move_mouse_to(x, y):
    # takes current mouse location and stores it
    while(True):
        try:
            curr_x, curr_y = pyautogui.position()
            # calculates the distance from current position to target position
            distance = int(((x - curr_x)**2 + (y - curr_y)**2)**0.5)
            # calculates a random time to make the move take based on the distance
            duration_of_move = (distance * random.random() / 2000) + 0.5
            # move the mouse to our position and takes the time of our duration just
            # calculated
            pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeInOutQuad)
            #pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeOutElastic)
            break
        except:
            print('paused for 10 seconds')
            time.sleep(10)

import win32api
import win32con

def scroll(value= 100):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0 , value, 0)
        return


def random_point(top_left, bottom_right):
    x = random.randint(top_left[0], bottom_right[0])
    y = random.randint(top_left[1], bottom_right[1])
    point = (x,y)
    return(point)



