from core import Screenshot

import win32gui
import win32ui
from ctypes import windll
from PIL import Image

from pprint import pprint
from core import GameConstants as gc
from core.RunescapeWindow import RunescapeWindow
from core import Keyboard
import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
import time

DEBUG = True


def match_images(template_path, compare_path):
    img_rgb = cv2.imread(template_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(compare_path, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.90
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        return (pt[0], pt[1], pt[0] + w, pt[1] + h)
    # cv2.imwrite('res.png', img_rgb)
    return None


def is_map_in_sync(base_client_infos, cur_client_infos):
    out_of_sync = False

    pprint(base_client_infos)
    # pprint(cur_client_infos)
    for client_name, client_info in cur_client_infos.iteritems():
        base_info = base_client_infos.get(client_name)
        base_map_file_path = base_info.get("MapFile")
        base_map_file_path = "C:/temp/test/edaeac32-edf2-42af-ac74-ac6db88b5ec3.png"
        client_map_file_path = client_info.get("MapFile")
        match_coordinates = match_images(base_map_file_path, client_map_file_path)
        if match_coordinates is None:
            return True

    if not out_of_sync:
        return False

        # print(base_map_file_path,client_map_file_path)
        # print()

        # pprint(base_client)
        # print client_name
        # client_info.get("MapFile")

    # template = cv2.imread(r'C:\Users\PPC\git\RS_BOT_2.0\lib\merchant_bot\anchor\exchange_history_icon.png', 0)
    # this(cur_img_rgb, base_img_rgb)
    # print match_images(cur_map_file, base_map_file)


def set_temp_folder():
    if not os.path.exists(gc.temp_folder):
        os.mkdir(gc.temp_folder)
        print("Directory ", gc.temp_folder, " Created ")
    else:
        print("Directory ", gc.temp_folder, " already exists")

    if os.path.exists(gc.temp_folder):
        return True
    return False


def stop_automation():
    Keyboard.hotkeys("alt", "f2")


def main():
    game_window = RunescapeWindow()

    base_client_info = game_window.get_client_main_data()

    # check_current_map()
    # pprint(base_client_info)
    cur_client_info = game_window.update_client_info()

    print is_map_in_sync(base_client_info, cur_client_info)

    # maps_in_sync = True
    # if DEBUG: print "Starting Main Loop"
    # while maps_in_sync:
    #     time.sleep(5)
    #
    #     map_diff_check = check_current_map(base_client_info, cur_client_info)
    #
    #     if map_diff_check is None:
    #         maps_in_sync = False


if __name__ == '__main__':
    set_temp_folder()
    main()
