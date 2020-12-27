import os
import time
import json
import subprocess
import time
import operator

from pprint import pprint
from core import GameConstants as gc
from core.RunescapeWindow import RunescapeWindow
from core import Keyboard
from core.send_mail import send_email
# from core import utils

import cv2
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import logging.config
from pyclick import HumanClicker

DEBUG = True


def match_images(template_path, compare_path, show_box=False):
    img_rgb = cv2.imread(template_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(compare_path, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = gc.template_match_threshold
    loc = np.where(res >= threshold)
    coord = None
    for pt in zip(*loc[::-1]):

        if show_box:
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

            cv2.rectangle(img_rgb, (pt[0] + 6, pt[1] + 16), (pt[0] + 7, pt[1] + 16), (255, 0, 255), 2)

        # coord = (pt[0], pt[1], pt[0] + w, pt[1] + h)
        coord = (int(pt[0]), int(pt[1]), int(pt[0] + w), int(pt[1] + h))

    if show_box:
        cv2.imwrite('sample.png', img_rgb)
    return coord


def is_map_in_sync(base_client_infos, cur_client_infos):
    # pprint(base_client_infos)
    # pprint(cur_client_infos)
    # for client_name, client_info in cur_client_infos.iteritems():
    for client_name, client_info in cur_client_infos.items():
        logger.info("Checking {0}".format(client_name))
        base_info = base_client_infos.get(client_name)
        base_map_file_path = base_info.get("MapFile")
        # base_map_file_path = "C:/temp/test/edaeac32-edf2-42af-ac74-ac6db88b5ec3.png"
        client_map_file_path = client_info.get("MapFile")
        match_coordinates = match_images(base_map_file_path, client_map_file_path)
        if match_coordinates is None:
            return False

    return True

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

    log_folder = "{0}/{1}".format(gc.temp_folder, "log")
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    if os.path.exists(gc.temp_folder):
        return True
    return False


def run_bot_cycle(logger):
    game_window = RunescapeWindow(logger=logger)
    game_window.set_main_client_data()

    base_client_info = game_window.get_client_main_data()
    if base_client_info is None:
        logger.info("Zero Instances of Runescape Detected")
        stop_MouseAndKeyBoardRecorder()
        return

    run_housecleaning(base_client_info)

    # check_current_map()
    # pprint(base_client_info)
    cur_client_info = game_window.update_client_info()

    # print is_map_in_sync(base_client_info, cur_client_info)

    logger.info("Starting Main Loop")
    maps_in_sync_status = is_map_in_sync(base_client_info, cur_client_info)

    filepath = "{0}/{1}".format(gc.temp_folder, 'file.json')
    fh = open(filepath)
    cache_json_data = json.load(fh)

    num_loop = 0
    while maps_in_sync_status:
        time.sleep(5)

        logger.info("Checking if Map is in Sync")
        cur_client_info = game_window.update_client_info()

        maps_in_sync_status = is_map_in_sync(base_client_info, cur_client_info)
        print(maps_in_sync_status)

        if not maps_in_sync_status:
            logger.info("OUT OF SYNC. Stopping.......")
        else:
            #     maps_in_sync_status = False
            logger.info("IN SYNC. Continuing....... ")

        num_loop += 1
        if num_loop % 10 == 0:
            run_housecleaning(base_client_info)

    if not maps_in_sync_status:
        send_notification(cache_json_data)
        stop_MouseAndKeyBoardRecorder()
    logger.info("Exit Process")


def launch_runescape_clients(logger):
    logger.info("Launching Runescape Clients")

    game_window = RunescapeWindow(logger=logger)

    cur_client_hwnds = game_window.get_all_client_hwnds()

    # while len(cur_client_hwnds) != gc.num_clients:

    if len(cur_client_hwnds) < gc.num_clients:
        num_launch = gc.num_clients - len(cur_client_hwnds)
        logger.info("Launching clients {0}".format(num_launch))
        for x in range(0, num_launch):
            client_pid = game_window.launch_client()
        time.sleep(60)
    elif len(cur_client_hwnds) > gc.num_clients:
        num_cull = len(cur_client_hwnds) - gc.num_clients

        temp_hwnds = cur_client_hwnds
        logger.info("Running too many clients. culling {0}".format(num_cull))
        for x in range(0, num_cull):
            cull_pid = game_window.convert_to_pid(temp_hwnds.pop(x)[0])
            game_window.close_client_by_pid(cull_pid)

    cur_client_hwnds = game_window.get_all_client_hwnds()

    # check dimenions to make sure the new clients are launched correctly
    for client_hwnds in cur_client_hwnds:

        client_dimensions = game_window.calculate_client_dimensions(client_hwnds[0])
        if client_dimensions is None:
            cull_pid = game_window.convert_to_pid(client_hwnds[0])
            game_window.close_client_by_pid(cull_pid)

    logger.info("Complete Launching Clients")
    return game_window.get_all_client_hwnds()


def shuffle_client_locations(logger):
    logger.info("Shuffle Client Locations")

    game_window = RunescapeWindow(logger=logger)
    cur_client_hwnds = game_window.get_all_client_hwnds()

    hwnds_list = []
    for client in cur_client_hwnds:
        hwnds_list.append(client[0])
        # print cur_client_hwnds[0][0]

    game_window.shuffle_clients(hwnds_list)


def run_recovery(logger):
    # base_map_file_path = r"C:\temp\test\ca8b7525-9399-42f7-9eee-c0fdf0431b06.png"
    # client_map_file_path = r"C:\temp\templates\seer_village_bank.png"
    # match_coordinates = match_images(base_map_file_path, client_map_file_path,show_box=True)
    # if match_coordinates is None:
    #     pass
    # print "YES", match_coordinates

    hc = HumanClicker()

    game_window = RunescapeWindow(logger=logger)
    game_window.set_main_client_data()

    pprint(game_window.get_client_main_data())
    base_client_info = game_window.get_client_main_data()

    # base_map_file_path = r"C:\temp\test\ca8b7525-9399-42f7-9eee-c0fdf0431b06.png"
    # base_map_file_path = base_client_info.get("MapFile")

    # for client_name, client_info in base_client_info.iteritems():

    all_recovery = True

    for client_name, client_info in base_client_info.items():
        logger.info("run recovery on {0}".format(client_name))
        base_info = base_client_info.get(client_name)
        base_map_file_path = base_info.get("MapFile")
        # base_map_file_path = "C:/temp/test/edaeac32-edf2-42af-ac74-ac6db88b5ec3.png"
        bank_anchor_file = r"C:\temp\templates\seer_village_bank.png"


        match_coordinates = match_images(base_map_file_path, bank_anchor_file, show_box=True)


        if match_coordinates is None:

            for x in range(5):
                match_coordinates = match_images(base_map_file_path, bank_anchor_file, show_box=True)
                if match_coordinates is None:
                    break
                else:
                    click_loc = tuple(
                        map(operator.add, base_info.get("ClientLoc"), base_info.get("GamePlayLocByClient")))
                    click_loc = tuple(map(operator.add, click_loc, base_info.get("MapLocByGamePlay")))
                    click_loc = tuple(map(operator.add, click_loc, match_coordinates))
                    click_loc = tuple(map(operator.add, click_loc, (6, 16, 7, 16)))

                    hc.move((click_loc[0], click_loc[1]), 2)
                    hc.click(click_loc[0], click_loc[1])
            logger.info("Recovery has failed. Ending Script")
            all_recovery = False
            continue
        else:
            click_loc = tuple(map(operator.add, base_info.get("ClientLoc"), base_info.get("GamePlayLocByClient")))
            click_loc = tuple(map(operator.add, click_loc, base_info.get("MapLocByGamePlay")))
            click_loc = tuple(map(operator.add, click_loc, match_coordinates))
            click_loc = tuple(map(operator.add, click_loc, (6, 16, 7, 16)))

            hc.move((click_loc[0], click_loc[1]), 2)
            hc.click(click_loc[0], click_loc[1])

    time.sleep(5)
    return all_recovery
    # bank_anchor_file= r"C:\temp\templates\seer_village_bank.png"
    #
    # match_coordinates = match_images(base_map_file_path, bank_anchor_file, show_box=True)
    # if match_coordinates is None:
    #     pass
    # print "YES", match_coordinates

    # cv2.rectangle(img_rgb, (pt[0] + 6, pt[1] + 16), (pt[0] + 7, pt[1] + 16), (255, 0, 255), 2)


def test(logger):
    # launch_runescape_clients(logger)
    # shuffle_client_locations(logger)
    # run_bot_cycle(logger)
    run_recovery(logger)
    # game_window = RunescapeWindow(logger=logger)
    # game_window.set_main_client_datla()
    #
    # pprint(game_window.get_client_main_data())

    # print game_window.calculate_client_location(198590)


def main(logger):
    # launch_runescape_clients(logger)
    # shuffle_client_locations(logger)
    run_bot_cycle(logger)


def run_housecleaning(base_client_info):
    logger.info("Running House Cleaning")
    important_files = []
    # for base_name, base_info in base_client_info.iteritems():
    for base_name, base_info in base_client_info.items():
        important_files.append(os.path.basename(base_info.get("GamePlayFile")))
        important_files.append(os.path.basename(base_info.get("MapFile")))
        important_files.append(os.path.basename(base_info.get("ClientFile")))

    filelist = [f for f in os.listdir(gc.temp_folder) if (f.endswith(".png") and f not in important_files)]

    for f in filelist:
        temp_remove = "{0}/{1}".format(gc.temp_folder, f)
        os.remove(temp_remove)
        logger.info("Removing {0}".format(temp_remove))


def stop_MouseAndKeyBoardRecorder():
    logger.info("Stopping Mouse And Keyboard Recording")
    Keyboard.hotkeys("alt", "f2")


def send_notification(json_data):
    username = json_data.get("user")
    password = json_data.get("pass")
    send = json_data.get("send")

    subject = "runescape bots are out of sync"
    msg = "runescape bots are out of sync"

    send_status = send_email(username, password, send, subject, msg)
    logger.info(send_status)


if __name__ == '__main__':
    # logging.config.fileConfig('logging.conf')

    # print "{0}/{1}".format(gc.temp_folder, 'logging.conf')
    logging.config.fileConfig("{0}/{1}".format(gc.temp_folder, 'logging.conf'))
    logger = logging.getLogger('MainLogger')
    str_time = '{:%Y-%m-%d}'.format(datetime.now())
    log_full_file = "C:/temp/log/{0}.log".format(str_time)
    fh = logging.FileHandler(log_full_file)
    # formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
    # formatter = logging.Formatter("%(asctime)s    %(levelname)s   %(module)s   %(message)s", "%Y-%m-%d %H:%M:%S")
    formatter = logging.Formatter("%(asctime)s     %(module)20s   %(message)s", "%H:%M:%S")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # logger.debug("test")

    set_temp_folder()

    logger.info("########################################################################")
    logger.info("------------------------- BOT WATCH STARTED ----------------------------")
    logger.info("########################################################################")

    main(logger)
    # test(logger)
