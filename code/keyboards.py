from aiogram import types
from aiogram.types import KeyboardButton


def keyboard_menu():
    buttons = [
        [KeyboardButton(text='Расписание📅'), 
        KeyboardButton(text='Выбор курса📎'),
        KeyboardButton(text='Зачетная книжка📂')],
        [KeyboardButton(text='Авторизация👤')]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def keyboard_course():
    buttons = [
        [types.KeyboardButton(text="1 курс"),
        types.KeyboardButton(text="2 курс")],
        [types.KeyboardButton(text="3 курс"),
        types.KeyboardButton(text="4 курс")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard