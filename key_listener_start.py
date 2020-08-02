import os
import sys
import subprocess
import psutil
from datetime import datetime
import logging.config
import time
from pprint import pprint
from pynput import keyboard
from core import Keyboard
from core import GameConstants as gc
import WatchStart as wsc

# logging.config.fileConfig('logging.conf')
logging.config.fileConfig("{0}/{1}".format(gc.temp_folder, 'logging.conf'))
logger = logging.getLogger('MainLogger')
str_time = '{:%Y-%m-%d}'.format(datetime.now())
log_full_file = "C:/temp/log/{0}.log".format(str_time)
fh = logging.FileHandler(log_full_file)
formatter = logging.Formatter("%(asctime)s     %(module)20s   %(message)s", "%H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)

# The key combination to check
CLOSE_COMBINATION = {keyboard.Key.alt_l, keyboard.Key.f2}

# The currently active modifiers
CUR_ACTIVE_MODIFIER = set()

DEBUG = True
BOT_WATCH_PID = None


def close_bot_watch_session():
    if BOT_WATCH_PID is None:
        os.system("taskkill /f /im python.exe")
    else:
        try:
            logger.info("Manually terminating process with pid {0}".format(BOT_WATCH_PID))
            p = psutil.Process(BOT_WATCH_PID)
            p.terminate()
        except psutil.NoSuchProcess:

            logger.info("close_bot_watch_session NoSuchProcess")
            pass


def stop_MouseAndKeyBoardRecorder():
    logger.info("Stopping Mouse And Keyboard Recording")
    Keyboard.hotkeys("alt", "f2")


def start_MouseAndKeyBoardRecorder():
    logger.info("Starting Mouse And Keyboard Recording")
    Keyboard.hotkeys("alt", "f3")


def on_press(key):
    if key in CLOSE_COMBINATION:
        CUR_ACTIVE_MODIFIER.add(key)
        if all(k in CUR_ACTIVE_MODIFIER for k in CLOSE_COMBINATION):
            logger.info("Alt-F2 Detected... Closing Runescape Bot Watch")
            time.sleep(10)    #make sure the everything is finished before killing the process
            close_bot_watch_session()
            listener.stop()

    # if key == keyboard.Key.esc:
    #     listener.stop()


def on_release(key):

    if key in CUR_ACTIVE_MODIFIER:
        CUR_ACTIVE_MODIFIER.remove(key)
    # try:
    #     CUR_ACTIVE_MODIFIER.remove(key)
    # except KeyError:
    #     logger.info("KeyError")
    #     pass


logger.info("########################################################################")
logger.info("########################################################################")
logger.info("----------------------- STARTING NEW SESSION ---------------------------")
logger.info("########################################################################")
logger.info("########################################################################")


# wsc.launch_runescape_clients(logger)
wsc.shuffle_client_locations(logger)

start_MouseAndKeyBoardRecorder()
# os.system()
# subprocess.Popen("{0} WatchStart.py".format(gc.python_path))


# p = subprocess.Popen([sys.executable, 'WatchStart.py'],
#                      stdout=subprocess.PIPE,
#                      stderr=subprocess.STDOUT,shell=True)

p = subprocess.Popen([sys.executable, 'WatchStart.py'], close_fds=True)

BOT_WATCH_PID = p.pid
logger.info("Starting WatchStart Subprocess on Pid {0}...".format(BOT_WATCH_PID))

for proc in psutil.process_iter():
    try:
        # Get process name & pid from process object.
        logger.info("processName {0} on {1}...".format(proc.name(),proc.pid))

        processName = proc.name()
        processID = proc.pid
        # print(processName, ' ::: ', processID)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        logger.info("NoSuchProcess Error")
        pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
