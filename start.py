from core import Screenshot

import win32gui
import win32ui
from ctypes import windll
from PIL import Image

from pprint import pprint
from core import GameConstants as gc
from core.RunescapeWindow import RunescapeWindow



if __name__ == '__main__':

    import os

    if not os.path.exists(gc.temp_folder):
        os.mkdir(gc.temp_folder)
        print("Directory ", gc.temp_folder, " Created ")
    else:
        print("Directory ", gc.temp_folder, " already exists")

    game_window = RunescapeWindow()
    game_window.setup_main_bot()

    # print game_coord
    # print game_coord[0]
    # print game_coord[1]
    # game_coord[2] +=game_coord[0]
    # game_coord[3] +=game_coord[1]
    # inventory_ss = Screenshot.this(game_coord[0], game_coord[1], game_coord[2], game_coord[3], "rgb")
    # cv2.imwrite("game_coord.png",inventory_ss)
    # print "done"
    # Screenshot.save("runelite.png",game_coord)
    # print  game_coord
