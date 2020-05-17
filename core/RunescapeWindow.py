from core import Screenshot

import win32gui
from pprint import pprint
from core import GameConstants as gc


class RunescapeWindow(object):
    """ Finds Runeloader Game Window"""

    def __init__(self, debug=True):

        self.debug = debug
        if self.debug: print "Setting Debug On"

        self.hwnd_dict = {}

        win32gui.EnumWindows(self.win_enum_handler, None)  # Getting each Individual hwnd for each open process
        # pprint(self.hwnd_dict)

        self.runescape_window_list = []
        self.number_clients = 0

    def win_enum_handler(self, hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            self.hwnd_dict[int(hwnd)] = win32gui.GetWindowText(hwnd)

    def setup_main_bot(self):
        if self.debug: print "Setting up main Runescape Window Data"
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

                self.runescape_window_list.append(temp_data_dict)
                num_clients += 1

        self.number_clients = num_clients
        pprint(self.runescape_window_list)

    def set_client_data(self, cur_client, hwnd):

        if self.debug: print "Setting up client {0}'s data".format(cur_client)

        temp_dict = {}
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        client_loc = (left, top, right, bot)
        temp_dict["ClientLoc"] = client_loc
        width = right - left
        height = bot - top

        if width != gc.default_client_size[0]:
            print "ERROR: Client Width set to {0}. Default is {1}".format(width, gc.default_client_size[0])
        if height != gc.default_client_size[1]:
            print "ERROR: Client Height set to {0}. Default is {1}".format(width, gc.default_client_size[1])

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

        return temp_dict