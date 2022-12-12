from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
ADMINS = [182418652, 936134134, 3202096]

TOKEN = "5780785373:AAHCsAO7lxUplEclqu_qwaVsLf6-EalnMtY"

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
