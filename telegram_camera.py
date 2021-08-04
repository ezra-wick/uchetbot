# -*- coding: utf-8 -*-
import os
import cv2
import imutils
import easyocr
import itertools
import telegram
import time
import json
import requests
import numpy as np
from PIL import Image, ImageEnhance
from aiogram.types import (ReplyKeyboardMarkup, 
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           InputMediaPhoto,
                           MediaGroup)

from aiogram import Bot, Dispatcher, executor, filters, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv 

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TOKEN2')
storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)
admins = [int(id_user) for id_user in os.getenv('admins').split(',') if id_user != '']


button = KeyboardButton('Смотреть')
translate = KeyboardButton('Транслировать')
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button).add(translate)

cancel_kb = InlineKeyboardMarkup(resize_keyboard=True)
back_button = InlineKeyboardButton('Отменить', callback_data='Отменить')
cancel_kb.insert(back_button)


def add_capture():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
    else:
        img_name = "camera.png"
        cv2.imwrite(img_name, frame)
    cam.release()
    cv2.destroyAllWindows()

def update_media(CHAT_ID, message_id, photo, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageMedia'

    params = {
    'chat_id': CHAT_ID,
    'message_id':message_id,
    'media': open(photo, 'rb'),

  }

    r = requests.post(url, data=params)

    print(r.reason)
    return r



@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await bot.send_message(message.from_user.id, 'Приветствую! Что будем делать?',
                                reply_markup=menu_kb)

@dp.message_handler()
async def menu(message: types.Message):
    chat_id = message.from_user.id

    if message.text == 'Смотреть':
        if chat_id in admins:
            add_capture()
            image = "camera.png"
            await bot.send_photo(message.from_user.id, open(image, 'rb'), 'Смотрим',
                                reply_markup=menu_kb)
        else:
            await bot.send_message(chat_id,
                                'У вас недостаточно прав!')         

    # if message.text == 'Транслировать':
    #     if chat_id in admins:
    #         text = 'Смотрим'
    #         add_capture()
    #         image = "camera.png"
    #         await bot.send_photo(message.from_user.id, open(image, 'rb'), text,
    #                             reply_markup=cancel_kb)
    #         stream = True
    #         id_message = message.message_id + 1
    #         while stream is True:  
    #             if text == "Смотрим":
    #                 text == '*'
    #             elif text == "*":
    #                 text == '**'
    #             elif text == "**":
    #                 text == '*'

    #             add_capture()
    #             time.sleep(1.5)
    #             update_media(chat_id, id_message, image, text)

    #             # await bot.edit_message_media(media=media, chat_id=chat_id, message_id=id_message, )
                # @dp.callback_query_handler(lambda c, back_button=back_button: c.data == back_button)
                # async def process_callback_button1(callback_query: types.CallbackQuery):
                #     stream = False


if __name__ == "__main__":
    # add_capture()
    executor.start_polling(dp, skip_updates=True)
