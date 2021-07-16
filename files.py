#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
from typing import final

months_nums = {
    '01':'Январь',
    '02':'Февраль',
    '03':'Март',
    '04':'Апрель',
    '05':'Май',
    '06':'Июнь',
    '07':'Июль',
    '08':'Август',
    '09':'Сентябрь',
    '10':'Октябрь',
    '11':'Ноябрь',
    '12':'Декабрь',
}

dimensions_list = ['кг.', 'г.', 'шт.', 'л.']

def get_now_time():
    return datetime.now().strftime("%Y%m%d%H%M")


def time_dict(time):
    year = time[:4]
    month = months_nums[time[4:6]]
    day = time[6:8]
    hour = time[8:10]
    minute = time[10:12]
    date_dict = {}
    date_list = [year, month, day, hour, minute]
    date_names = ['год', 'месяц', 'день', 'час', 'минуты']
    for name, date in zip(date_names, date_list):
        date_dict[name] = date
    return date_dict


def time_readable(time):
    year = time[:4]
    month = months_nums[time[4:6]]
    day = time[6:8]
    hour = time[8:10]
    minute = time[10:12]
    return f'{day} {month} {year}г. в {hour}:{minute}'


def load_data(name):
    path = os.path.abspath(os.getcwd() + '/data/' + name) 
    with open(path, 'r') as file:
        return json.load(file)


def save_data(name, data, mode='a'):
    path = os.path.abspath(os.getcwd() + '/data/' + name) 
    with open(path, mode) as file:
        json.dump(data, file)   


if __name__ == "__main__":
    pass