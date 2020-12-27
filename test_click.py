import unittest
# from pyclick.humanclicker import HumanClicker
import pyautogui
import random
from random import choice,randint,triangular

if __name__ == '__main__':
    # width, height = pyautogui.size()
    # toPoint = random.randint(width // 2, width - 1), random.randint(height // 2, height - 1)
    # hc = HumanClicker()
    # hc.move(toPoint)
    #
    # randS = triangular(.1, .5)
    # hc.move(x, y, randS)




    # x1, y1, x2, y2 = skills[skill]
    # x, y = Mouse.genCoords(x1, y1, x2, y2)
    # # Mouse.moveTo(x,y)
    # # randS = triangular(.1, .5)
    # # hc.move(toPoint)
    #
    # from pyclick import HumanClicker
    #
    # # initialize HumanClicker object
    # hc = HumanClicker()
    #
    # # move the mouse to position (100,100) on the screen in approximately 2 seconds
    # hc.move((100, 100), 2)
    #
    # # mouse click(left button)
    # hc.click()
    # print toPoint
    # x =  100
    # y =  500
    # hc.move(x, y, randS)

    print ("ADGLASDLIASDLAF")
    # from pyclick import HumanClicker

    from pyclick import HumanClicker
    # from pyclick import

    # initialize HumanClicker object
    hc = HumanClicker()

    # move the mouse to position (100,100) on the screen in approximately 2 seconds


    pyautogui.moveTo(1300, 200)
    hc.move((2300, 1000), 2)

    # mouse click(left button)
    hc.click()




    # pyautogui.moveTo(100, 500, 2)

    # skill = "magic"
    # skills = {
    #     'attack': 0, 'hitpoints': 0, 'mining': 0,
    #
    #     'strength': 0, 'agility': 0, 'smithing': 0,
    #
    #     'defence': 0, 'herblore': (620, 295, 662, 311), 'fishing': 0,
    #
    #     'ranged': 0, 'thieving': 0, 'cooking': 0,
    #
    #     'prayer': 0, 'crafting': (621, 358, 664, 373), 'firemaking': 0,
    #
    #     'magic': (557, 388, 602, 402), 'fletching': (620, 389, 666, 406), 'woodcutting': 0,
    #
    #     'runecraft': 0, 'slayer': 0, 'farming': 0,
    #
    #     'construction': 0, 'hunter': 0
    # }
    #
    #
    #
    # x1, y1, x2, y2 = skills[skill]
    # # x, y = Mouse.genCoords(x1, y1, x2, y2)
    # print random.randint(width // 2, width - 1), random.randint(height // 2, height - 1)
    # y = 500
    # # Mouse.moveTo(x,y)
    # randS = triangular(.1, .5)
    # hc.move(x, y, randS)