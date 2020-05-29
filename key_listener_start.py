import os
import psutil
from pprint import pprint
from pynput import keyboard

# The key combination to check
CLOSE_COMBINATION = {keyboard.Key.alt_l, keyboard.Key.f2}

# The currently active modifiers
CUR_ACTIVE_MODIFIER = set()

DEBUG = True


def close_bot_watch_session():
    os.system("taskkill /f /im python.exe")

def on_press(key):
    if key in CLOSE_COMBINATION:
        CUR_ACTIVE_MODIFIER.add(key)
        if all(k in CUR_ACTIVE_MODIFIER for k in CLOSE_COMBINATION):
            if DEBUG: print "Alt-F2 Detected... Closing Runescape Bot Watch"
            listener.stop()
            close_bot_watch_session()

    # if key == keyboard.Key.esc:
    #     listener.stop()


def on_release(key):
    try:
        CUR_ACTIVE_MODIFIER.remove(key)
    except KeyError:
        pass

for proc in psutil.process_iter():
    try:
        # Get process name & pid from process object.
        processName = proc.name()
        processID = proc.pid
        print(processName , ' ::: ', processID)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
PROCNAME = "python.exe"


if DEBUG: print "Keyboard Listener Start"
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
