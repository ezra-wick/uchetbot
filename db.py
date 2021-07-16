#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
from files import *


user_db = 'User.json'
product_db = 'Product.json'
operation_db = 'Operation.json'
finance_db = 'Finance.json'
delivery_db = 'Delivery.json'


def add_worker(telegram_id, name, phone, role, salary,
               start_working=None, stop_working=None,
               day_worker=None, all_salary=None):
    try:
        user_dict = get_all_workers()
    except:
        user_dict = {}
    user_info_dict = {}
    user_info_dict['telegram_id'] = telegram_id
    user_info_dict['телефон'] = phone
    user_info_dict['должность'] = role

    try:
        get_worker_info(name)['дата добавления']
        user_info_dict['дата добавления'] = get_worker_info(name)['дата добавления']
    except:
        time_start = get_now_time()
        user_info_dict['дата добавления'] = time_start

    
    user_info_dict['дата начала работы'] = start_working
    user_info_dict['дата окончания работы'] = stop_working
    user_info_dict['отработано смен'] = day_worker
    user_info_dict['зарплата'] = salary
    user_info_dict['всего получено'] = all_salary
    user_dict[name] = user_info_dict
    save_data(user_db, user_dict, mode='w+')


def get_worker_info(name):
    return load_data(user_db)[name]
    


def get_all_workers():
    return load_data(user_db)

def find_by_id(telegram_id):
    for name, dict_value in get_all_workers().items():
        for value_name, value in dict_value.items():
            if value_name == 'telegram_id' and value == telegram_id:
                return name

def del_worker(name):
    all_workers = get_all_workers()
    all_workers.pop(name)
    save_data(user_db, all_workers, mode='w+')


def get_product_info(name):
    return load_data(product_db)[name]


def get_all_products():
    return load_data(product_db)


def del_product(name):
    all_products = get_all_products()
    all_products.pop(name)
    save_data(product_db, all_products)


def add_product(name, dimension, price, quantity=None,
                in_sale=True, description=None,
                category=None, image=None):
    product_dict = {}
    product_info_dict = {}
    try:
        if load_data(product_db):
            product_count = len(list(load_data(product_db).keys()))
            if len(str(product_count)) == 1:
                product_id = '000' + str(product_count)
            elif len(str(product_count)) == 2:
                product_id = '00' + str(product_count)
            elif len(str(product_count)) == 3:
                product_id = '0' + str(product_count)
            product_info_dict['id'] = product_id
    except:
        product_id = 0000
        product_info_dict['id'] = product_id
    
    product_info_dict['в продаже'] = in_sale
    product_info_dict['кол-во'] = quantity
    product_info_dict['ед. измерения'] = dimension

    product_info_dict['цена'] = price
    product_info_dict['описание'] = description
    product_info_dict['категория'] = category
    product_info_dict['изображение'] = image
    try:
        get_product_info(name)['дата добавления']
        product_info_dict['дата добавления'] = get_product_info(name)['дата добавления']
    except:
        time_start = get_now_time()
        product_info_dict['дата добавления'] = time_start
    product_dict[name] = product_info_dict
    save_data(product_db, product_dict)


def load_deliveries():
    return load_data(delivery_db)


def add_delivery(product_dict):
    try:
        delivery_dict = load_deliveries()
    except:
        delivery_dict = {}
    time_start = get_now_time()
    delivery_dict[time_start] = product_dict
    save_data(product_db, delivery_dict)


def add_operation(user, operation_type, result='', value=''):
    time_of_operation = get_now_time()
    operation = f'{time_of_operation}_{user}_{operation_type}_{result}_{value}\n'
    with open(os.path.abspath(os.getcwd() + '/data/operations.txt'), 'a', encoding='utf-8') as file:
        file.write(operation)
        file.close()


def load_operations():
    with open(os.path.abspath(os.getcwd() + '/data/operations.txt'), 'r', encoding='utf-8') as file:
        refile = file.read()
        file.close()
    return refile.split('\n')


def humanize_text(dict, double=True):
    empty_text = ''
    for key, value in dict.items():
        if value is not None:
            if double:
                empty_text += key + ":\n"
                for name_of_data, data in value.items():
                    if data is not None:
                        if len(str(data)) == 12:
                            try:
                                data = time_readable(str(data))
                            except:
                                continue
                        empty_text += f'{name_of_data} - {data}.\n'
                empty_text += '\n'
            else:
                if len(str(value)) == 12:
                    try:
                        value = time_readable(str(value))
                    except:
                        continue
                empty_text += f'{key} - {value}.\n'

    return empty_text

if __name__ == "__main__":
    add_worker(155138061, 'Тофик', 89260777963, 'Разработчик', 202207101919, 202307101919)
    print(get_worker_info('Тофик'))
    add_product('Арбуз', 100, 'кг', 50, description='очень вкусный')
    print(get_product_info('Арбуз'))  
    print(list(load_data(product_db).keys()))
    del_product('Арбуз')
    print(list(load_data(product_db).keys()))