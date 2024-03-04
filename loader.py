import os
from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv, dotenv_values
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

load_dotenv()

ADMINS = list(int(i) for i in os.getenv('ADMINS').split(', '))
TOKEN = os.getenv('TOKEN')

movie_ganres = {
    "comedy": "Комедия",
    "fantasy": "Фантастика",
    "horror": "Ужасы",
    "action": "Боевик",
    "melodrama": "Мелодрама",
    "mystic": "Мистика",
    "detective": "Детектив",
    "military": "Военное"
}
movie_ganres_rus = {
    'комедия': 'comedy',
    'фантастика': 'fantasy',
    'ужасы': 'horror',
    'боевик': 'action',
    'мелодрама': 'melodrama',
    'мистика': 'mystic',
    'детектив': 'detective',
    'военное': 'military'
}


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot=bot, storage=storage)
