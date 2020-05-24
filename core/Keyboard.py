# Keyboard.py
import pyautogui
import time
import random
### My Modules
import RandTime


def type_this(strings):
    """Types the passed characters with random pauses in between strokes"""
    for s in strings:
        # delay between key presses--key UP/DOWN
        # autopy.key.toggle(s, True)
        pyautogui.keyDown(s)
        RandTime.randomTime(2, 7)
        pyautogui.keyUp(s)
        # delay after key UP--next key


def press(button):
    if button == 'enter':
        pyautogui.keyDown('enter')
        RandTime.randomTime(2, 7)
        pyautogui.keyUp('enter')
    elif button == 'f1' or button == 'spec':
        pyautogui.keyDown('f1')
        RandTime.randomTime(2, 7)
        pyautogui.keyUp('f1')
    elif button == 'f2' or button == 'stats':
        pyautogui.keyDown('f2')
        RandTime.randomTime(2, 7)
        pyautogui.keyUp('f2')
    elif button == 'f4' or button == 'equipment':
        pyautogui.keyDown('f4')
        RandTime.randomTime(2, 7)
        pyautogui.keyUp('f4')
    elif button == 'f6' or button == 'magic':
        pyautogui.keyDown('f6')
        RandTime.randomTime(2, 7)
        pyautogui.keyUp('f6')
    elif button == 'f8' or button == 'friends':
        pyautogui.keyDown('f8')
        RandTime.randomTime(2, 7)
        pyautogui.keyUp('f8')

    elif button == 'exit' or button == 'inventory':
        pyautogui.keyDown('esc')
        RandTime.randomTime(2, 7)
        pyautogui.keyUp('esc')


def hold_key(key):
    pyautogui.keyDown(key)
    RandTime.randomTime(650, 750)
    # RandTime.randomTime(0, 5)
    pyautogui.keyUp(key)
    print "done"


def hotkeys(control, key):
    pyautogui.keyDown(control)
    RandTime.randomTime(2, 7)
    pyautogui.keyDown(key)
    RandTime.randomTime(2, 7)
    pyautogui.keyUp(key)
    pyautogui.keyUp(control)
    # pyautogui.hotkey('ctrl', 'c')
