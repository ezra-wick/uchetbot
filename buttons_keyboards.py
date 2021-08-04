from aiogram.types import ParseMode, \
                          ReplyKeyboardMarkup, \
                          KeyboardButton, \
                          InlineKeyboardButton, \
                          InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, executor, filters, types
from db import *

EnterForLeader_btn = KeyboardButton('Вход для руководителя 🔑')
EnterForСashier_btn = KeyboardButton('Вход для кассира 👷')

Back_btn2 = KeyboardButton('Назад ◀')
Back_btn3 = KeyboardButton('Назад ⏪')

worker_menu_text = 'Сотрудники 👷'
all_workers_info_text = 'Отчет по сотрудникам 📑'
get_worker_info_text = 'Информация о сотруднике 🔍'
add_worker_text = 'Добавить сотрудника ➕'
change_worker_text = 'Изменить данные сотрудника 🟨'
delete_worker_text = 'Удалить сотрудника ❌'

Worker_menu_btn = KeyboardButton(worker_menu_text)
All_workers_info_btn = KeyboardButton(all_workers_info_text)
Get_worker_info_btn = KeyboardButton(get_worker_info_text)
Add_worker_btn = KeyboardButton(add_worker_text)
Change_worker_btn = KeyboardButton(change_worker_text)
Delete_worker_btn = KeyboardButton(delete_worker_text)
worker_menu_kb = (ReplyKeyboardMarkup(resize_keyboard=True).add(Get_worker_info_btn)
                                                           .add(All_workers_info_btn)
                                                           .add(Add_worker_btn)
                                                           .add(Change_worker_btn)
                                                           .add(Delete_worker_btn)
                                                           .add(Back_btn2))


product_menu_text = 'Товары 📦'
get_product_info_text = 'Информация о товаре 🔍'
add_product_text = 'Добавить товар ➕'
change_product_text = 'Изменить данные товара 🟨'
delete_product_text = 'Удалить товар ❌'

Product_menu_btn = KeyboardButton(product_menu_text)
Get_product_info_btn = KeyboardButton(get_product_info_text)
Add_product_btn = KeyboardButton(add_product_text)
Change_product_btn = KeyboardButton(change_product_text)
Delete_product_btn = KeyboardButton(delete_product_text)
product_menu_kb = (ReplyKeyboardMarkup(resize_keyboard=True).add(Get_product_info_btn)
                                                            .add(Add_product_btn)
                                                            .add(Change_product_btn)
                                                            .add(Delete_product_btn)
                                                            .add(Back_btn2))


delivery_menu_text = 'Поставки 🚛'
add_delivery_value_text = 'Добавить ➕'
change_delivery_info_text = 'Изменить 🚛'
get_delivery_info_text = 'Информация 🔍'
delivery_cancel_text = 'Отменить последнюю поставку ❌'

Delivery_menu_btn = KeyboardButton(delivery_menu_text)
Add_delivery_value_btn = KeyboardButton(add_delivery_value_text)
Change_delivery_info_btn = KeyboardButton(change_delivery_info_text)
Get_delivery_info_btn = KeyboardButton(get_delivery_info_text)
Delivery_cancel_btn = KeyboardButton(delivery_cancel_text)
delivery_menu_kb = (ReplyKeyboardMarkup(resize_keyboard=True).add(Add_delivery_value_btn)
                                                             .add(Change_delivery_info_btn)
                                                             .add(Get_delivery_info_btn)
                                                             .add(Delivery_cancel_btn)
                                                             .add(Back_btn2))


Get_operations_btn = KeyboardButton('События 📰')
Get_info_btn = KeyboardButton('Создать отчёт 📑')



calc_btn = KeyboardButton('Калькулятор 🧮')
Back_btn = KeyboardButton('Назад ↩')

main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(EnterForLeader_btn).add(EnterForСashier_btn)
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)#.add(btnPoems)

leader_menu_kb = (ReplyKeyboardMarkup(resize_keyboard=True).add(Delivery_menu_btn)
                                                           .add(Product_menu_btn)
                                                           .add(Worker_menu_btn)
                                                           .add(Get_operations_btn)
                                                           .add(Get_info_btn)
                                                           .add(calc_btn)
                                                           .add(Back_btn))

                                                           
cashier_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(calc_btn).add(Back_btn)

keys = InlineKeyboardMarkup(resize_keyboard=True)
second_poems = InlineKeyboardMarkup(resize_keyboard=False)

calculator_kb = InlineKeyboardMarkup(resize_keyboard=True)

list_of_calculator = ['с', '%', '◀', '-', '+', '/', '7', '8', '9', '4', '5', '6', '1', '2', '3', ',', '0', 'x', 'отмена', '=']
list_of_numbers = [7, 8, 9, 4, 5, 6, 1, 2, 3, 0,]
operators = ['%', '-', '+', '/', 'x']
new_button = InlineKeyboardButton('Выйти', callback_data='+')

calculator_field_kb = InlineKeyboardMarkup(resize_keyboard=True)
calculator_field_kb.insert(InlineKeyboardButton('Пусто', callback_data='Ответ: '))  

dimension_kb = InlineKeyboardMarkup(resize_keyboard=True)
for dimension in dimensions_list:
    dimension_kb.insert(InlineKeyboardButton(dimension, callback_data=dimension))  
