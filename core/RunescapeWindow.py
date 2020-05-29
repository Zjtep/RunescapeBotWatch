from core import Screenshot

import win32gui
from pprint import pprint
from core import GameConstants as gc

import logging.config
from datetime import datetime


# logger.debug("TGGEAAAAAAAAAAAAAST")


class RunescapeWindow(object):
    """ Finds Runeloader Game Window"""

    def __init__(self, debug=True, logger=None):

        if logging == None:
            logging.basicConfig()
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.setLevel(logging.INFO)
        else:
            self.logger = logger

        self.debug = debug
        self.logger.info("Setting Debug On")

        self.hwnd_dict = {}

        win32gui.EnumWindows(self.win_enum_handler, None)  # Getting each Individual hwnd for each open process
        # pprint(self.hwnd_dict)

        self.client_main_data = self.update_client_info()

    def win_enum_handler(self, hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            self.hwnd_dict[int(hwnd)] = win32gui.GetWindowText(hwnd)

    def update_client_info(self):
        # if self.debug: print "Setting up main Runescape Window Data"
        # self.logger.info("Setting up main Runescape Window Data")

        return_clients = {}
        num_clients = 0
        for hwnd, process in self.hwnd_dict.iteritems():

            if gc.client_name in process:
                cur_client = "Window{0}".format(num_clients)

                temp_data_dict = {cur_client: {}}
                temp_data_dict[cur_client]["Hwnd"] = hwnd

                client_data = self.set_client_data(cur_client, hwnd)

                temp_data_dict[cur_client].update(client_data)
                # Change the line below depending on whether you want the whole window
                # or just the client area.
                # left, top, right, bot = win32gui.GetClientRect(hwnd)

                return_clients.update(temp_data_dict)
                num_clients += 1

        return return_clients
        # pprint(self.client_main_data)

    def set_client_data(self, cur_client, hwnd):

        # self.logger.info("Setting up client {0}'s data".format(cur_client))

        temp_dict = {}
        left, top, right, bot = win32gui.GetWindowRect(hwnd)

        client_loc = (left, top, right, bot)
        temp_dict["ClientLoc"] = client_loc
        width = right - left
        height = bot - top
        # win32gui.MoveWindow(hwnd, 0, 0, 809, 534, True)
        if width != gc.default_client_size[0]:
            self.logger.error("ERROR: Client Width set to {0}. Default is {1}".format(width, gc.default_client_size[0]))
        if height != gc.default_client_size[1]:
            self.logger.error("ERROR: Client Height set to {0}. Default is {1}".format(width, gc.default_client_size[1]))

        client_size = (0, 0, width, height)
        temp_dict["ClientDimension"] = client_size
        client_imgrgb = Screenshot.hdms_this(hwnd, left, top, right, bot)
        temp_dict["ClientFile"] = Screenshot.save_image(client_imgrgb)

        # Needs to crop out the actually gameplay location to find the mini map. It will not be accurate if we use just the client location because that could be resized
        gameplay_loc = (0, gc.client_menu_height, width - gc.client_menu_width, height)
        temp_dict["GamePlayLocByClient"] = gameplay_loc
        temp_dict["GamePlayDimension"] = (0, 0, width - gc.client_menu_width, height - gc.client_menu_height)

        gameplay_imrgb = Screenshot.crop_image(client_imgrgb, gameplay_loc[0], gameplay_loc[1], gameplay_loc[2],
                                               gameplay_loc[3])

        temp_dict["GamePlayFile"] = Screenshot.save_image(gameplay_imrgb)

        # crop out the actual mini map
        map_loc = (0, gc.client_menu_height, width - gc.client_menu_width, height)

        map_loc = gc.map_loc
        temp_dict["MapLocByGamePlay"] = map_loc

        map_imrgb = Screenshot.crop_image(gameplay_imrgb, map_loc[0], map_loc[1], map_loc[2], map_loc[3])
        temp_dict["MapFile"] = Screenshot.save_image(map_imrgb)

        # ---------- mini map testing---------------
        # testfile = "C:/temp/test/3f3a3b67-6891-4fea-8845-a33824456d8c.png"
        # Screenshot.open_and_crop_image(testfile, map_loc[0], map_loc[1], map_loc[2],
        #                                map_loc[3])
        # -----------------------------------------

        # win32gui.MoveWindow(hwnd, 0, 0, 760, 500, True)

        return temp_dict

    def get_client_main_data(self):
        return self.client_main_data
