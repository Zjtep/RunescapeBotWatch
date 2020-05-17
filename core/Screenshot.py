#!/usr/bin/python2
import uuid
import cv2
import numpy as np
import pyautogui
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from core import GameConstants as gc


def crop(img_rgb, coord):
    return img_rgb[coord[1]:coord[3], coord[0]:coord[2]]
    # return img_rgb[x2:y2, x1:y1]


def this(coord):
    # creates widht & height for screenshot region

    x1 = coord[0]
    y1 = coord[1]
    x2 = coord[2]
    y2 = coord[3]
    w = x2 - x1
    h = y2 - y1
    # PIL format as RGB
    img = pyautogui.screenshot(region=(x1, y1, w, h))  # X1,Y1,X2,Y2
    # im.save('screenshot.png')

    # Converts to an array used for OpenCV
    img = np.array(img)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return rgb_img


def save(file_name, coord):
    image = this(coord)
    cv2.imwrite(file_name, image)


def show_rectangle(img, coord_list):
    cv2.rectangle(img, (coord_list[0], coord_list[1]), (coord_list[2], coord_list[3]), (0, 255, 100), 1)


def display(img):
    cv2.imshow('Detected', img)
    cv2.waitKey(0)


def hdms_this(hwnd, left, top, right, bot):
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
    # print result

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
        # temp_file = "{0}/{1}.png".format(gc.temp_folder, str(uuid.uuid4()))
        # PrintWindow Succeeded
        # im.save(temp_file)
        # return temp_file

        return im

    return


def open_and_crop_image(file_name, left, top, right, bot, output=False):
    img = Image.open(file_name)
    # area = (50, 0, 300, 300)
    area = (left, top, right, bot)
    cropped_img = img.crop(area)

    if output is True:
        temp_file = "{0}/{1}.png".format(gc.temp_folder, str(uuid.uuid4()))
        # cropped_img.save(temp_file)
        cropped_img.save(temp_file, quality=100)
        return temp_file

    cropped_img.show()
    return


def crop_image(img_rgb, left, top, right, bot):
    area = (left, top, right, bot)
    cropped_img = img_rgb.crop(area)

    return cropped_img


def save_image(img_rgb):
    temp_file = "{0}/{1}.png".format(gc.temp_folder, str(uuid.uuid4()))

    # img_rgb.save(temp_file)
    img_rgb.save(temp_file, quality=100)
    return temp_file

# if __name__ == '__main__':
#     Screenshot.save("temp/blah.png",(0,0,100,100))
