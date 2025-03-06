from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import router as client_router
# Импортируем get-ы

load_dotenv()
# token = getenv('bot_token')

# Создаём объект бота и диспетчера (маршрутизатора)
bot = Bot(token = getenv('bot_token'))
dp = Dispatcher()
dp.include_router(client_router)



dp.run_polling(bot)