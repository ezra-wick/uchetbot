#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
import time
from typing import KeysView
from files import get_now_time, load_data, save_data
from db import *
from aiogram import Bot, Dispatcher, executor, filters, types
from aiogram.types import ParseMode, \
                          ReplyKeyboardMarkup, \
                          KeyboardButton, \
                          InlineKeyboardButton, \
                          InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv 
from aiogram.dispatcher import FSMContext
from buttons_keyboards import *
from states import ProductState, WorkerState, DeliveryState

load_dotenv()

storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
admins = [int(id_user) for id_user in os.getenv('admins').split(',') if id_user != '']
cashiers = [int(id_user) for id_user in os.getenv('admins').split(',') if id_user != '']
dp = Dispatcher(bot, storage=storage)

path = '/data/daily_info.json'


next_page = '»»»'

collectCalcList = []


def str_to_num(str):
    try:
        num = float(str.replace(',', '.'))
    except:
        num = float(str)
    return num

def calc_method(num1, num2, operator):
    answer = 0
    if operator == '+':
        answer = num1 + num2
    if operator == 'x':
        answer = round(num1 * num2, 1)
    if operator == '/':
        answer = round(num1 / num2, 1)
    if operator == '-':
        answer = num1 - num2

    collectCalcList = answer
    return answer

def calc_func(list):
    first_numbers = 0
    second_numbers = 0
    all_as_str = ''.join(list)
    operator_method = ''
    for operator in operators:
        try:
            splitted = all_as_str.split(operator)
            first_numbers = str_to_num(splitted[0])
            second_numbers = str_to_num(splitted[1])
            operator_method = operator
            print(operator)
        except:
            continue
    answer = calc_method(first_numbers, second_numbers, operator_method)
    return answer

@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    visitors_db = 'Visitors.json'
    dict_info = {}
    user_id = message.from_user.id
    try:
        first_name = find_by_id(user_id)
    except:
        first_name = message.from_user.first_name

    date_visit = get_now_time()
    try:
        visitor_dict = load_data(visitors_db)
        dict_info['визиты'] = load_data(visitors_db)[first_name]['визиты'] + date_visit + ','
    except:
        visitor_dict = {}
        dict_info['визиты'] = date_visit + ','

    dict_info['id'] = user_id
    visitor_dict[first_name] = dict_info
    save_data(visitors_db, visitor_dict)

    add_operation(first_name, 'ЗАПУСК_БОТА', result = True)
    await bot.send_message(message.from_user.id, 'Приветствую! Выберите куда войти!',
                                reply_markup=main_kb)


for sign in list_of_calculator:
    calculator_kb.insert(InlineKeyboardButton(sign, callback_data=sign))  
    @dp.callback_query_handler(lambda c, sign=sign: c.data == sign)
    async def calculate(callback_query: types.CallbackQuery):
        # if len(collectCalcList) > 1:
        #     if callback_query.data == collectCalcList[-1]:
        #         callback_query.data = callback_query.data + collectCalcList[-1]
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id - 1
        if callback_query.data == '=':
            calculator_field_new_kb = InlineKeyboardMarkup(resize_keyboard=True)
            answer = calc_func(collectCalcList)
            collectCalcList.clear()
            calculator_field_new_kb.insert(InlineKeyboardButton(answer, callback_data=answer))
            text = f'⬇  Ваш  ответ  ⬇'
            await bot.edit_message_text(text, chat_id, message_id, reply_markup=calculator_field_new_kb)

        elif callback_query.data == 'с':
            calculator_field_new_kb = InlineKeyboardMarkup(resize_keyboard=True)
            if len(collectCalcList) == 0:
                calculator_field_new_kb.insert(InlineKeyboardButton('Пусто', callback_data='Пусто'))
                text = f'📌 ---  здесь будет ответ ---  📌'
                await bot.edit_message_text(text, chat_id, message_id, reply_markup=calculator_field_new_kb)
            else:
                collectCalcList.clear()
                calculator_field_new_kb.insert(InlineKeyboardButton('Пусто', callback_data='Пусто'))
                text = f'⬇  Ваш  ответ  ⬇'
                await bot.edit_message_text(text, chat_id, message_id, reply_markup=calculator_field_new_kb)

        elif callback_query.data == '◀':
            calculator_field_new_kb = InlineKeyboardMarkup(resize_keyboard=True)
            if len(collectCalcList) == 1:
                calculator_field_new_kb.insert(InlineKeyboardButton('Пусто', callback_data='Пусто'))
                text = f'📌 ---  здесь будет ответ ---  📌'
                await bot.edit_message_text(text, chat_id, message_id, reply_markup=calculator_field_new_kb)
            else:
                collectCalcList.pop()
                collected_signs = ''.join(collectCalcList)
                calculator_field_new_kb.insert(InlineKeyboardButton(collected_signs, callback_data=collected_signs))
                text = f'📌 ---  здесь будет ответ ---  📌'
                await bot.edit_message_text(text, chat_id, message_id, reply_markup=calculator_field_new_kb)
        
        else:
            collectCalcList.append(callback_query.data)
            calculator_field_new_kb = InlineKeyboardMarkup(resize_keyboard=True)
            collected_signs = ''.join(collectCalcList)
            calculator_field_new_kb.insert(InlineKeyboardButton(collected_signs, callback_data=collected_signs))
            text = f'💲  ---   введите   цифры   ---  💲'
            await bot.edit_message_text(text, chat_id, message_id, reply_markup=calculator_field_new_kb)




@dp.message_handler()
async def menu(message: types.Message, state=FSMContext):
    chat_id = message.from_user.id
    first_name = find_by_id(chat_id)

    if message.text == 'Вход для руководителя 🔑' or message.text == 'Назад ◀':
        if chat_id in admins:
            add_operation(first_name, 'МЕНЮ_РУКОВОДИТЕЛЯ', result = True)
            await bot.send_message(chat_id,
                                'Переходим в меню',
                                reply_markup=leader_menu_kb)
        else:
            add_operation(first_name, 'МЕНЮ_РУКОВОДИТЕЛЯ', result = False)
            await bot.send_message(chat_id,
                                'У вас недостаточно прав!') 

    if message.text == 'Вход для кассира 👷':
        if chat_id in (cashiers or admins):
            add_operation(first_name, 'МЕНЮ_КАССИРА', result = True)
            await bot.send_message(chat_id,
                                'Переходим в меню',
                                reply_markup=cashier_menu_kb)
        else:
            add_operation(first_name, 'МЕНЮ_КАССИРА', result = False)
            await bot.send_message(chat_id,
                                'У вас недостаточно прав!') 
    
    if message.text == 'Назад ↩':
        add_operation(first_name, 'ГЛАВНОЕ_МЕНЮ', result = True)
        await bot.send_message(message.from_user.id,
                               'Приветствую! Выберите куда войти!',
                               reply_markup=main_kb)

    if message.text == 'Калькулятор 🧮':
        add_operation(first_name, 'КАЛЬКУЛЯТОР', result = True)
        await bot.send_message(message.from_user.id,
                               '📌 ---  здесь будет ответ ---  📌',
                               reply_markup=calculator_field_kb)

        await bot.send_message(message.from_user.id,
                               '💲  ---   введите   цифры   ---  💲',
                               reply_markup=calculator_kb)

    if chat_id in admins:
        if message.text == 'Сотрудники 👷':
            add_operation(first_name, 'СОТРУДНИКИ', result = True)
            await bot.send_message(message.from_user.id,
                                'Здесь можно выполнить любые операции с сотрудниками.',
                                reply_markup=worker_menu_kb)     
        
        if message.text == all_workers_info_text:
            try:
                all_workers = get_all_workers()
                all_workers = humanize_text(all_workers)
                await bot.send_message(message.from_user.id,
                                    all_workers,
                                    reply_markup=worker_menu_kb)
            except:
                await bot.send_message(message.from_user.id,
                                    'У вас ещё нет сотрудников.',
                                    reply_markup=worker_menu_kb)

        if message.text == get_worker_info_text:
            try:
                special_kb = InlineKeyboardMarkup(resize_keyboard=True)
                special_list = list(get_all_workers().keys())
                for worker in special_list:
                    special_kb.insert(InlineKeyboardButton(worker, callback_data=worker))
                await bot.send_message(message.from_user.id,
                                    'Выберите сотрудника',
                                    reply_markup=special_kb)
            except:
                await bot.send_message(message.from_user.id,
                                    'У вас ещё нет сотрудников.',
                                    reply_markup=worker_menu_kb)

        if message.text == add_worker_text:
            await bot.send_message(message.from_user.id,
                                  'Введите имя нового сотрудника')
            await WorkerState.WORKER_NAME.set()

        if message.text == change_worker_text:
            pass
        if message.text == delete_worker_text:
            try:
                special_kb = InlineKeyboardMarkup(resize_keyboard=True)
                special_list = list(get_all_workers().keys())
                for worker in special_list:
                    special_kb.insert(InlineKeyboardButton(worker, callback_data=worker+'><'))
                await bot.send_message(message.from_user.id,
                                    'Выберите сотрудника',
                                    reply_markup=special_kb) 
            except:
                await bot.send_message(message.from_user.id,
                                    'У вас ещё нет сотрудников.',
                                    reply_markup=worker_menu_kb)

        if message.text == 'Товары 📦':
            add_operation(first_name, 'ТОВАРЫ', result = True)
            await bot.send_message(message.from_user.id,
                                'Здесь можно выполнить любые операции с товарами',
                                reply_markup=product_menu_kb) 

        if message.text == get_product_info_text:
            try:
                product_kb = InlineKeyboardMarkup(resize_keyboard=True)
                product_list = list(get_all_products().keys())
                for product in product_list:
                    product_kb.insert(InlineKeyboardButton(product, callback_data=product))
                await bot.send_message(message.from_user.id,
                                        'Выберите товар',
                                        reply_markup=product_kb) 
            except:
                await bot.send_message(message.from_user.id,
                                    'У вас ещё нет товаров.',
                                    reply_markup=product_menu_kb)

        if message.text == add_product_text:
            await bot.send_message(message.from_user.id,
                                  'Введите имя нового товара')
            await ProductState.PRODUCT_NAME.set()

        if message.text == change_product_text:
            pass

        if message.text == delete_product_text:
            try:
                product_kb = InlineKeyboardMarkup(resize_keyboard=True)
                product_list = list(get_all_products().keys())
                for product in product_list:
                    product_kb.insert(InlineKeyboardButton(product, callback_data=product+'><'))
                await bot.send_message(message.from_user.id,
                                        'Выберите товар',
                                        reply_markup=product_kb) 
            except:
                await bot.send_message(message.from_user.id,
                                    'У вас ещё нет сотрудников.',
                                    reply_markup=product_menu_kb)


        if message.text == 'Поставки 🚛':
            add_operation(first_name, 'ПОСТАВКИ', result = True)
            await bot.send_message(message.from_user.id,
                                'Что у нас сегодня?',
                                reply_markup=delivery_menu_kb)  

        if message.text == delivery_menu_text:
            pass
        if message.text == add_delivery_value_text:
            pass
        if message.text == change_delivery_info_text:
            pass    
        if message.text == get_delivery_info_text:
            pass
      

        if message.text == 'События 📰':
            operations = load_operations()
            text_to_sent = ''
            if len(operations) > 20:
                operations = operations[-20:]    
            for operation in operations:
                if operation != '':
                    date_of_operation = time_readable(operation[:12]) + '\n'
                    text = operation[12:].replace('_', ' ') + '\n\n'
                    text_to_sent += date_of_operation + text
            add_operation(first_name, 'СОБЫТИЯ', result = True)
            await bot.send_message(message.from_user.id,
                                   text_to_sent) 

        if message.text == 'Создать отчёт 📑':
            add_operation(first_name, 'СОЗДАТЬ_ОТЧЁТ', result = True)
            await bot.send_message(message.from_user.id,
                                '📌   здесь будет ответ   📌',
                                reply_markup=calculator_field_kb)


    
''' WORKER STATE HANDLER '''   

@dp.message_handler(state=WorkerState.WORKER_NAME)
async def worker_name(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = callback_query.text
    await bot.send_message(callback_query.from_user.id,
                                  'Введите телефон сотрудника')
    await WorkerState.WORKER_PHONE.set()


@dp.message_handler(state=WorkerState.WORKER_PHONE)
async def worker_phone(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = callback_query.text
    await bot.send_message(callback_query.from_user.id,
                                  'Введите должность сотрудника')
    await WorkerState.WORKER_ROLE.set()


@dp.message_handler(state=WorkerState.WORKER_ROLE)
async def worker_role(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['role'] = callback_query.text
    await bot.send_message(callback_query.from_user.id,
                           'Введите ТЕЛЕГРАМ ID сотрудника')
    await WorkerState.WORKER_TG_ID.set()


@dp.message_handler(state=WorkerState.WORKER_TG_ID)
async def worker_tg_id(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['tg_id'] = callback_query.text
    await bot.send_message(callback_query.from_user.id,
                           'Введите зарплату сотрудника')
    await WorkerState.WORKER_SALARY.set()


@dp.message_handler(state=WorkerState.WORKER_SALARY)
async def worker_salary(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name = data['name']
        phone = data['phone']
        role = data['role']
        tg_id = int(data['tg_id'])
        salary = callback_query.text
        add_worker(tg_id, name, phone, role, salary)
        await bot.send_message(callback_query.from_user.id,
                            'Сотрудник успешно добавлен!')
    await state.finish()


''' PRODUCT STATE HANDLER '''   

@dp.message_handler(state=ProductState.PRODUCT_NAME)
async def product_name(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    state = dp.get_current().current_state() 
    async with state.proxy() as data:
        data['name'] = callback_query.text
    await bot.send_message(callback_query.from_user.id,
                        'Выберите ед. измерения товара',
                        reply_markup=dimension_kb)

@dp.message_handler(state=ProductState.PRODUCT_DIMENSION)
async def product_dimension(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['dimension'] = callback_query.data
    await bot.send_message(callback_query.from_user.id,
                        'Введите стоимость товара')
    await ProductState.PRODUCT_PRICE.set()


@dp.message_handler(state=ProductState.PRODUCT_PRICE)
async def product_price(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name = data['name']
        dimension = data['dimension']
        price = callback_query.text
        add_product(name, dimension, price)
        await bot.send_message(callback_query.from_user.id,
                            'Товар успешно добавлен!')
    await state.finish()


''' DELIVERY STATE HANDLER '''   

@dp.message_handler(state=DeliveryState.DELIVERY_QUANTITY)
async def update_points(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()


async def stop(state):
    current_state = await state.get_state()
    if current_state is None:
        return


workers_list = list(get_all_workers().keys())
for worker in workers_list:
    @dp.callback_query_handler(lambda c, worker=worker: c.data == worker)
    async def info_worker(callback_query: types.CallbackQuery):
        worker_info = get_worker_info(callback_query.data)
        worker_info = callback_query.data + ':\n' + humanize_text(worker_info, double=False)
        await bot.send_message(callback_query.from_user.id,
                                worker_info,
                                reply_markup=worker_menu_kb)


    @dp.callback_query_handler(lambda c, worker=worker: c.data == worker + '><')
    async def delete_worker(callback_query: types.CallbackQuery):
        del_worker(callback_query.data.replace('><',''))
        await bot.send_message(callback_query.from_user.id,
                                "Сотрудник удален!")


product_list = list(get_all_products().keys())
for product in product_list:
    @dp.callback_query_handler(lambda c, product=product: c.data == product)
    async def info_product(callback_query: types.CallbackQuery):
        product_info = get_product_info(callback_query.data)
        product_info = callback_query.data + ':\n' + humanize_text(product_info, double=False)
        await bot.send_message(callback_query.from_user.id,
                                product_info,
                                reply_markup=product_menu_kb)


    @dp.callback_query_handler(lambda c, product=product: c.data == product + '><')
    async def product_worker(callback_query: types.CallbackQuery):
        del_product(callback_query.data.replace('><',''))
        await bot.send_message(callback_query.from_user.id,
                                "Товар удален!")

for dimension in dimensions_list:
    @dp.callback_query_handler(lambda c, dimension=dimension: c.data == dimension)
    async def set_dimension(callback_query: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['dimension'] = callback_query.data
        await bot.send_message(callback_query.from_user.id,
                            'Введите стоимость товара')
        await ProductState.PRODUCT_PRICE.set()

        

if __name__ == "__main__":
    num = 0
    executor.start_polling(dp, skip_updates=True)
