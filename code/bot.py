import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types.input_file import FSInputFile
from aiogram import F
from classes import *
from configs.config import *
from keyboards import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

global course
course = ''
chat_id = ''


@dp.message(Command("start"))
async def cmd_stardasdsat(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile('./images/logo_to_chat.png', 'rb'))
    await message.answer("<b>Привет!🎉</b> Добро пожаловать в бота по упрощению учебной жизни в Финансовом Университете при Правительстве РФ КФ\n\n"
                        "Здесь ты можешь посмотреть свое расписание нажатием кнопки <i><b>Расписание</b></i>, выбрать свой курс кнопкой <i><b>Выбор курса</b></i>.\n\n"
                        "На данном этапе это не итоговая версия, некоторые функции будут дополняться, следите за обновлениями 🚀", reply_markup= keyboard_menu(), parse_mode='HTML')

@dp.message(F.text == 'Выбор курса📎')
async def cmd_course(message: types.Message):
    await message.answer("Выбери свой курс", reply_markup=keyboard_course())

@dp.message(F.text.lower() == "1 курс")
async def course1(message: types.Message):
    global course 
    course = '1'
    await message.answer('Отлично, я записал!', reply_markup= keyboard_menu())

@dp.message(F.text.lower() == "2 курс")
async def course2(message: types.Message):
    global course 
    course = '2'
    await message.answer('Отлично, я записал!', reply_markup= keyboard_menu())

@dp.message(F.text.lower() == "3 курс")
async def course3(message: types.Message):
    global course 
    course = '3'
    await message.answer('Отлично, я записал!', reply_markup= keyboard_menu())

@dp.message(F.text.lower() == "4 курс")
async def course4(message: types.Message):
    global course 
    course = '4'
    await message.answer('Отлично, я записал!', reply_markup= keyboard_menu())

@dp.message(F.text == 'Расписание📅')
async def cmd_sheduler(message: types.Message):
    global course
    if course != '':
        response = univer(course).schedule()
        document = FSInputFile(response)
        await bot.send_document(message.chat.id, document, reply_markup= keyboard_menu())
    else:
        await message.answer('Ошибка! Для начала укажите свой курс!', reply_markup= keyboard_menu())

@dp.message(Command("whatcourse"))
async def start(message: types.Message):
    await message.answer("Ты учишься на: " + course)

@dp.message(F.text == 'Авторизация👤')
async def kn(message):
    await bot.send_message(message.chat.id, f'Введите логин и пароль! \n\nОбразец: \nЛогин:пароль')

@dp.message(F.text.lower()[3:6] == 'dot' )
async def logpass(message):
    log_data = message.text.split(':')
    login = security().encrypt(log_data[0])
    password = security().encrypt(log_data[1])
    log_data = [login, password]
    chat_id = message.chat.id
    await message.answer(univer(course).database_auth(log_data, chat_id), reply_markup= keyboard_menu())

@dp.message(F.text == 'Зачетная книжка📂')
async def grades(message:types.Message):
    chat_id = message.chat.id
    if univer(course).check_user_id_to_parsing(chat_id) is False:
        await message.answer('Для начала авторизуйтесь!')
    else:
        try:
            response = univer(course).parsing(univer(course).check_user_id_to_parsing(chat_id))
            await message.answer(response, reply_markup= keyboard_menu())
        except Exception as e:
            await message.answer(f'Произошла ошибка: {e}', reply_markup= keyboard_menu())


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())