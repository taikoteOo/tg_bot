from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.enums import ParseMode

from api import get_vacancies, get_courses, get_weathers
from keyboards import simple_keyboard


router = Router()

@router.message(F.text == 'Кнопка 1')
async def progress_bin_1(message: Message):
    await message.answer(text='Вы нажали кнопку № 1')#, reply_markup=ReplyKeyboardRemove()) Если добавить, прячут кнопки

@router.message(F.text == 'Кнопка 2')
async def progress_bin_2(message: Message):
    await message.answer(text='Вы нажали кнопку № 2')#, reply_markup=ReplyKeyboardRemove())

@router.message(Command(commands=['keyboard']))
async def process_keyboard_command(message: Message):
    await message.answer(text='Привет. Сделай выбор', reply_markup=simple_keyboard())

@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет. Спроси у меня что-нибудь')

@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Привет. Выбери нужное действие')

@router.message(Command(commands=['weather']))
async def process_weather_command(message: Message):
    await message.answer('Погода на сегодня:')

@router.message(Command(commands=['vacancies']))
async def process_vacancies_command(message: Message):
    data = get_vacancies()
    await message.answer('3 случайные вакансии Python-разработчика')
    for item in data:
        text = f'<b>{item["name"]}</b>\nЗарплата: {item["salary"]}\nДата публикации: {item["created_at"]}\nСсылка: {item["url"]}'
        await message.answer(text, parse_mode=ParseMode.HTML,  disable_web_page_preview=True) # Последнее выключает предпросмотор ссылок

@router.message(Command(commands=['courses']))
async def process_courses_command(message: Message):
    await message.answer('Курс доллара на сегодня')