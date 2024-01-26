from PIL import Image
import PIL.ImageOps
import pytesseract
import cv2
import numpy as np
import argparse
import imutils
import requests
import time
import configparser
import tkinter
import sys
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox

def catchrep(i):
    #建立session
    user_agent = UserAgent()
    headers={ 'user-agent': user_agent.random }

    cap_headers = {
        'Host' : 'cart.books.com.tw',
        'Referer' : 'https://cart.books.com.tw/member/login',
        'user-agent': user_agent.random
    }
    session_requests = requests.session()
    response = session_requests.get('https://cart.books.com.tw/member/regen_captcha', headers=cap_headers)
    captcha = response.text

    cap_pic_url = 'https://cart.books.com.tw/member/captcha_login?' + captcha

    response = session_requests.get(cap_pic_url, headers=cap_headers)
    pic_filename = str(i)+'.png'
    with open(pic_filename, "wb") as file:  # 開啟資料夾及命名圖片檔
            file.write(response.content)
    return pic_filename

if __name__ == "__main__":

    i = 0
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    while True:
        i = i + 1
        pic_filename = catchrep(i)
        image = cv2.imread(pic_filename)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])

        # define range of green color in HSV 
        lower_green = np.array([50,100,100])
        upper_green = np.array([70,255,255])

        # define range of red color in HSV 
        lower_red = np.array([-10,100,100])
        upper_red = np.array([10,255,255])

        # Threshold the HSV image to get only blue colors
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        text = pytesseract.image_to_string(mask_blue, lang='eng')
        captcha = text[0:4]
        if len(captcha) == 4:
            print(captcha)
            text_filename = str(i)+'.txt'
            with open(text_filename, "w") as file:
                file.write(captcha)
            break

        # Threshold the HSV image to get only green colors
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        text = pytesseract.image_to_string(mask_green, lang='eng')
        captcha = text[0:4]
        if len(captcha) == 4:
            print(captcha)
            text_filename = str(i)+'.txt'
            with open(text_filename, "wb") as file:  # 開啟資料夾及命名圖片檔
                file.write(captcha)
            break

        # Threshold the HSV image to get only red colors   
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        text = pytesseract.image_to_string(mask_red, lang='eng')
        captcha = text[0:4]
        if len(captcha) == 4:
            print(captcha)
            text_filename = str(i)+'.txt'
            with open(text_filename, "wb") as file:  # 開啟資料夾及命名圖片檔
                file.write(captcha)
            break

        # Bitwise-AND mask and original image
#        res_blue = cv2.bitwise_and(image,image, mask= mask_blue)
#        res_green = cv2.bitwise_and(image,image, mask= mask_green)
#        res_red = cv2.bitwise_and(image,image, mask= mask_red)
#        cv2.imshow('frame',image)
        cv2.imshow('mask_blue)',mask_blue)
        cv2.imshow('mask_green',mask_green)
        cv2.imshow('mask_red',mask_red)
#        cv2.imshow('res_blue',res_blue)
#        cv2.imshow('res_green',res_green)
#        cv2.imshow('res_red',res_red)
        cv2.waitKey(3)
        cv2.destroyAllWindows()
    print('success!!')
