from core import Screenshot

import win32gui
import win32ui
from ctypes import windll
from PIL import Image

from pprint import pprint
from core import GameConstants as gc


class RunescapeWindow(object):
    """ Finds Runeloader Game Window"""

    def __init__(self, debug=True):

        self.debug = debug
        if self.debug: print "Setting Debug On"

        self.hwnd_dict = {}

        win32gui.EnumWindows(self.winEnumHandler, None)  # Getting each Individual hwnd for each open process
        # pprint(self.hwnd_dict)

    def winEnumHandler(self, hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            self.hwnd_dict[int(hwnd)] = win32gui.GetWindowText(hwnd)

    def get_all_coordinates(self):

        for hwnd, process in self.hwnd_dict.iteritems():
            if process == gc.client_name:

                # Change the line below depending on whether you want the whole window
                # or just the client area.
                # left, top, right, bot = win32gui.GetClientRect(hwnd)
                left, top, right, bot = win32gui.GetWindowRect(hwnd)
                w = right - left
                h = bot - top

                print w, h


if __name__ == '__main__':
    game_window = RunescapeWindow()
    game_window.get_all_coordinates()

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
