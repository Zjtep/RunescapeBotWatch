


def test1():
    # import ctypes
    #
    # EnumWindows = ctypes.windll.user32.EnumWindows
    # EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    # GetWindowText = ctypes.windll.user32.GetWindowTextW
    # GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    # IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    #
    # titles = []
    #
    #
    # def foreach_window(hwnd, lParam):
    #     if IsWindowVisible(hwnd):
    #         length = GetWindowTextLength(hwnd)
    #         buff = ctypes.create_unicode_buffer(length + 1)
    #         GetWindowText(hwnd, buff, length + 1)
    #         # titles.append(buff.value)
    #         titles.append((hwnd, buff.value))
    #     return True
    #
    #
    # EnumWindows(EnumWindowsProc(foreach_window), 0)
    #
    # print(titles)

    import win32gui

    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print (int(hwnd), win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(winEnumHandler, None)

    import win32gui
    import win32ui
    from ctypes import windll
    from PIL import Image

    hwnd = win32gui.FindWindow(None, 'runelite')

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    print result

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        # PrintWindow Succeeded
        im.save("test.png")

#
# from pynput import keyboard
#
# # The key combination to check
# COMBINATION = {keyboard.Key.alt, keyboard.Key.f1}
#
# # The currently active modifiers
# current = set()
#
#
# def on_press(key):
#     if key in COMBINATION:
#         current.add(key)
#         if all(k in current for k in COMBINATION):
#             print('All modifiers active!')
#     if key == keyboard.Key.esc:
#         listener.stop()
#
#
# def on_release(key):
#     try:
#         current.remove(key)
#     except KeyError:
#         pass
#
#
# print "in"
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()
#
#
#

#!/usr/bin/env python
# import logging
# logger = logging.getLogger(__name__)
#
# def main():
#     print ":Wwtf"
#     logger.debug('This is a debug message.')
#     logger.info('This is an info message.')
#
#
# if __name__=='__main__':
#     main()
#


import logging.config

# logging.config.fileConfig('logging.conf')
# logger = logging.getLogger('pyApp')
#
# logger.info('testing')


from datetime import datetime

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('MainLogger')

blah = '{:%Y-%m-%d}'.format(datetime.now())
adsf = "C:/temp/log/{0}.log".format(blah)
fh = logging.FileHandler(adsf)
# formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
formatter = logging.Formatter("%(asctime)s    %(levelname)s   %(module)s   %(message)s","%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.debug("TGGEST")



#> ERROR:__main__:Division by zero problem
#> Traceback (most recent call last):
#>   File "<ipython-input-16-a010a44fdc0a>", line 12, in divide
#>     out = x / y
#> ZeroDivisionError: division by zero
#> ERROR:__main__:None

# class MockButton:
#     def __init__(self, *keys):
#         self.combination = {*keys}
#         self.currently_pressed = set()
#         self.is_pressed = False
#
#         listener = Listener(on_press=self._on_press, on_release=self._on_release)
#         listener.start()
#
#     def _on_press(self, key):
#         if key in self.combination:
#             self.currently_pressed.add(key)
#
#         if self.currently_pressed == self.combination:
#             self.is_pressed = True
#             print('pressed!')
#
#     def _on_release(self, key):
#         try:
#             self.currently_pressed.remove(key)
#
#             if self.is_pressed and len(self.currently_pressed) == 0:
#                 self.is_pressed = False
#                 print('released!')
#
#         except KeyError:
#             pass
#
# if __name__ == '__main__':
#     btn = MockButton(keyboard.Key.alt, keyboard.Key.ctrl)
#     input()
#



# from pynput import keyboard
# import datetime
#
# # The key combinations to check
# # COMBINATIONS = [
# #     {keyboard.Key.alt_l, keyboard.KeyCode(char='c')},
# #     {keyboard.Key.alt_l, keyboard.KeyCode(char='c')}
# # ]
#
# COMBINATIONS = [
#     {keyboard.Key.alt_l, keyboard.Key.f2},
#     {keyboard.Key.alt_l, keyboard.Key.f2}
# ]
# # The currently active modifiers
# current = set()
#
# tnow = datetime.datetime.now()
# tcounter = 0
#
# def on_press(key):
#     if any([key in comb for comb in COMBINATIONS]):
#         current.add(key)
#         if any(all(k in current for k in comb) for comb in COMBINATIONS):
#             global tnow
#             global tcounter
#             tcounter += 1
#             if datetime.datetime.now() - tnow < datetime.timedelta(seconds=1):
#                 if tcounter > 1:
#                     tcounter = 0
#                     main_function()
#             else:
#                 tnow = datetime.datetime.now()
#     if key == keyboard.Key.esc:
#         listener.stop()
#
#
# def on_release(key):
#     try:
#         current.remove(key)
#     except KeyError:
#         pass
#
# def main_function():
#     print('Main function fired!')
#     # rest of your code here...
#
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()