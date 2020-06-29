import os
import time
import json

from pprint import pprint
from core import GameConstants as gc
from core.RunescapeWindow import RunescapeWindow
from core import Keyboard
from core.send_mail import send_email
import cv2
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import logging.config

DEBUG = True


def match_images(template_path, compare_path):
    img_rgb = cv2.imread(template_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(compare_path, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = gc.template_match_threshold
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        return (pt[0], pt[1], pt[0] + w, pt[1] + h)
    # cv2.imwrite('res.png', img_rgb)
    return None


def is_map_in_sync(base_client_infos, cur_client_infos):
    # pprint(base_client_infos)
    # pprint(cur_client_infos)
    for client_name, client_info in cur_client_infos.iteritems():
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


def main(logger):
    game_window = RunescapeWindow(logger=logger)

    base_client_info = game_window.get_client_main_data()
    if not base_client_info:
        logger.debug("Zero Instances of Runescape Detected")
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
        print maps_in_sync_status

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


def run_housecleaning(base_client_info):
    logger.info("Running House Cleaning")
    important_files = []
    for base_name, base_info in base_client_info.iteritems():
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
