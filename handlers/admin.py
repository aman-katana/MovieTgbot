from aiogram import types
from keyboards import admin_kb
from aiogram import Dispatcher
from loader import ADMINS, dp, bot
from data_base.base import add_movie
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


async def admin(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer("Панель администратора", reply_markup=admin_kb.admin_kb)
    else:
        await message.answer("Такой команды нет или она пока не реализованна 404")


class FSMload(StatesGroup):
    video = State()
    name = State()
    ganre = State()
    desc = State()
    date = State()
    country = State()
    producer = State()
    actors = State()
    confirm = State()


# @dp.message_handler(Text(startswith="Загрузить", ignore_case=True))
async def load(message: types.Message):
    await message.answer("Отправьте видео фильма", reply_markup=admin_kb.stop_load)
    await FSMload.video.set()


async def cancel_load(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    await callback.message.answer("Загрузка фильма отменена")


# @dp.message_handler(content_types=['video'], state=FSMload.video)
async def load_video(message: types.Message, state: FSMContext):
    video = message.video.file_id
    # print(f"video ok, {video}")
    # await bot.send_video(message.from_user.id, video=video)

    async with state.proxy() as data:
        data["video"] = video
    await FSMload.next()
    await message.answer("Введите НАЗВАНИЕ фильма", reply_markup=admin_kb.stop_load)


# @dp.message_handler(state=FSMload.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMload.next()
    await message.answer("Введите Жанр фильма", reply_markup=admin_kb.ganre_kb)


# @dp.callback_query_handler(state=FSMload.ganre)
async def load_ganre(callbaack: types.CallbackQuery, state: FSMContext):
    await callbaack.message.delete()
    async with state.proxy() as data:
        data["ganre"] = callbaack.data.split("_")[1]
    await FSMload.next()
    await callbaack.message.answer("Введите Описание фильма", reply_markup=admin_kb.stop_load)
    await callbaack.answer()


# @dp.message_handler(state=FSMload.desc)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["desc"] = message.text
    await FSMload.next()
    await message.answer("Введите год производства ", reply_markup=admin_kb.stop_load)


# @dp.message_handler(state=FSMload.date)
async def load_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await FSMload.next()
    await message.answer("Введите страну производства ", reply_markup=admin_kb.stop_load)


# @dp.message_handler(state=FSMload.country)
async def load_country(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["country"] = message.text
    await FSMload.next()
    await message.answer("Введите режисёров фильма", reply_markup=admin_kb.stop_load)


# @dp.message_handler(state=FSMload.producer)
async def load_producer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["producer"] = message.text
    await FSMload.next()
    await message.answer("Введите Актёров фильма", reply_markup=admin_kb.stop_load)


# @dp.message_handler(state=FSMload.actors)
async def load_actors(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["actors"] = message.text
        movie = data
        await message.answer_video(movie["video"],
                                   caption=f"""<b>{movie['name']}</b>
                \n{movie['description']}
                \nЖанр: {movie['ganre']}\nГод: {movie['date']}\nСтрана: {movie['country']}
                \nРежисёр|Продюсер: {movie['producer']}\nАктёры: {movie['actors']}""")

    await message.answer("Подтвердите загрузку : ", reply_markup=admin_kb.confirm_kb)
    await FSMload.next()


# @dp.message_handler(state=FSMload.confirm)
async def load_confirm(message: types.Message, state: FSMContext):
    if message.text.startswith("Подтвердить"):
        async with state.proxy() as data:

            await add_movie(data)
        await message.answer("Фильма отправлен на загрузку", reply_markup=admin_kb.admin_kb)
    else:
        await message.answer("Загурзка фильма не осуществлена", reply_markup=admin_kb.admin_kb)
    await state.finish()


def register_admin_handler(dp: Dispatcher):
    dp.register_message_handler(admin, commands=["admin"])
    dp.register_message_handler(admin, Text(equals="admin", ignore_case=True))

    # Загрузить
    dp.register_message_handler(load, Text(startswith="Загрузить", ignore_case=True))
    # Остановка загрузки
    dp.register_callback_query_handler(cancel_load, Text(startswith="stop_load"), state="*")

    dp.register_message_handler(load_video, content_types=['video'], state=FSMload.video)
    dp.register_message_handler(load_name, state=FSMload.name)
    dp.register_callback_query_handler(load_ganre, state=FSMload.ganre)
    dp.register_message_handler(load_desc, state=FSMload.desc)
    dp.register_message_handler(load_date, state=FSMload.date)
    dp.register_message_handler(load_country, state=FSMload.country)
    dp.register_message_handler(load_producer, state=FSMload.producer)
    dp.register_message_handler(load_actors, state=FSMload.actors)
    dp.register_message_handler(load_confirm, state=FSMload.confirm)
