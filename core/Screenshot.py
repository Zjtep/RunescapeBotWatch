#!/usr/bin/python2
import cv2
import numpy as np
import pyautogui

def crop(img_rgb,coord):
    return img_rgb[coord[1]:coord[3], coord[0]:coord[2]]
    # return img_rgb[x2:y2, x1:y1]

def this(coord):
    # creates widht & height for screenshot region

    x1=coord[0]
    y1=coord[1]
    x2=coord[2]
    y2=coord[3]
    w = x2 - x1
    h = y2 - y1
    # PIL format as RGB
    img = pyautogui.screenshot(region=(x1,y1,w,h)) #X1,Y1,X2,Y2
    #im.save('screenshot.png')

    # Converts to an array used for OpenCV
    img = np.array(img)


    rgb_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return rgb_img


def save(file_name,coord):
    image = this(coord)
    cv2.imwrite(file_name,image)


def show_rectangle(img,coord_list):
    cv2.rectangle(img, (coord_list[0], coord_list[1]), (coord_list[2], coord_list[3]), (0, 255, 100), 1)

def display(img):
    cv2.imshow('Detected', img)
    cv2.waitKey(0)

# if __name__ == '__main__':
#     Screenshot.save("temp/blah.png",(0,0,100,100))