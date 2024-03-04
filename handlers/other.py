import datetime
from aiogram import types
from aiogram import Dispatcher
from keyboards.client_kb import home_kb
from data_base.base import add_user
from aiogram.dispatcher.filters import Text


# @dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Добро пожаловать.\nЭтот бот был разработан в качестве кусового проекта", reply_markup=home_kb)
    await add_user(user_id=message.from_user.id, user_name=message.from_user.username, user_date=datetime.date.today())


# @dp.message_handler(Text(equals="Назад"))
async def back(message: types.Message):
    await message.answer("Главное меню", reply_markup=home_kb)


async def other(message: types.Message):
    await message.answer("Такой команды нет или она пока не реализованна", reply_markup=home_kb)


def register_other_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(back, Text(startswith="Назад", ignore_case=True))
    dp.register_message_handler(other)
