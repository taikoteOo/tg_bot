from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def simple_keyboard():
    btn_1 = KeyboardButton(text='Кнопка 1')
    btn_2 = KeyboardButton(text='Кнопка 2')

    #                              нормализует размер     скрывает после нажатия
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[btn_1, btn_2]])
    return keyboard

def vacancies_keyboard():
    any_vacancies = KeyboardButton(text='Любые')
    with_salary = KeyboardButton(text='С указанием заработной платы')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[any_vacancies, with_salary]])
    return keyboard