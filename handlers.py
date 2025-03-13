from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.enums import ParseMode

from api import get_vacancies, get_courses, get_weathers
from api.vacancies_api import get_salary_vacancies
from keyboards import simple_keyboard, vacancies_keyboard


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

def show_vacancies(item):
    text = (f'<b>{item["Название"]}</b>\n'
                f'Заработная плата:\n'
                f'От: {item["Заработная плата"]["От"]} {item["Заработная плата"]["Валюта от"]}\n'
                f'До: {item["Заработная плата"]["До"]} {item["Заработная плата"]["Валюта до"]}\n'
                f'Дата публикации: {item["Дата публикации"]}\n'
                f'Ссылка: {item["url"]}')
    return text

@router.message(F.text == 'Любые')
async def progress_any(message: Message):
    data = get_vacancies()
    await message.answer('3 случайные вакансии на Python')
    for item in data:
        text = show_vacancies(item)
        await message.answer(text, parse_mode=ParseMode.HTML,
                             disable_web_page_preview=True) # Последнее выключает предпросмотор ссылок

@router.message(F.text == 'С указанием заработной платы')
async def progress_with_salary(message: Message):
    data = get_salary_vacancies()
    await message.answer('3 случайные вакансии на Python c указанием заработной платы')
    for item in data:
        text = show_vacancies(item)
        await message.answer(text, parse_mode=ParseMode.HTML,
                             disable_web_page_preview=True)

@router.message(Command(commands=['vacancies']))
async def process_vacancies_command(message: Message):
    await message.answer(text='Какие вакансии?', reply_markup=vacancies_keyboard())

@router.message(Command(commands=['courses']))
async def process_courses_command(message: Message):
    await message.answer('Курс доллара на сегодня')