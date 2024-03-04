from aiogram import types
from data_base import base
from aiogram import Dispatcher
from keyboards import client_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import dp, movie_ganres, movie_ganres_rus
from aiogram.dispatcher.filters.state import State, StatesGroup


# Жанры ================================================================================================================
async def genres(message: types.Message):
    await message.answer("Выберите жанр который вам интересен : ", reply_markup=client_kb.choose_kb)


@dp.callback_query_handler(Text(startswith="choose_"))
async def genre_show(callback: types.CallbackQuery):
    genre = callback.data.split("_")[1]

    if genre == "stop":
        await callback.message.delete()
        await callback.message.answer("Отмена выбора", reply_markup=client_kb.home_kb)
    else:
        movie_lst = await base.get_movie_genre(genre)
        await callback.message.edit_text("Выберите фильм из списка :",
                                         reply_markup=client_kb.movies_kb(movie_lst, genre))

    await callback.answer()


@dp.callback_query_handler(Text(startswith="genre_page"))
async def genre_choose(callback: types.CallbackQuery):
    action = callback.data.split("_")[2]
    page = callback.data.split("_")[3]
    genre = callback.data.split("_")[4]
    if action == "prev" and int(page) >= 2:
        movie_lst = await base.get_movie_genre(genre, int(page) - 1)
        await callback.message.edit_text("Выберите фильм из списка :",
                                         reply_markup=client_kb.movies_kb(movie_lst, genre, page=int(page) - 1))
    elif action == "next":
        movie_lst = await base.get_movie_genre(genre, int(page) + 1)
        await callback.message.edit_text("Выберите фильм из списка :",
                                         reply_markup=client_kb.movies_kb(movie_lst, genre, page=int(page) + 1))
    elif action == "back":
        await callback.message.edit_text("Выберите жанр который вам интересен : ",
                                         reply_markup=client_kb.choose_kb)
    await callback.answer()


@dp.callback_query_handler(Text(startswith="show_movie"))
async def movie_show(callback: types.CallbackQuery):
    movie_id = callback.data.split("_")[2]
    await callback.message.delete()

    movie = await base.get_movie_id(movie_id)
    movie = dict(movie[0][0])

    ganre = movie_ganres[movie['ganre']]

    await callback.message.answer_video(movie["video"],
                                        caption=f"""<b>{movie['name']}</b>
        \n{movie['description']}
        \nЖанр: {ganre}\nГод: {movie['date']}\nСтрана: {movie['country']}
        \nРежисёр|Продюсер: {movie['producer']}\nАктёры: {movie['actors']}""",
                                        reply_markup=client_kb.like_kb(movie_id, movie["likes"]))


class SearchM(StatesGroup):
    look = State()


# Поиск ================================================================================================================
async def search(message: types.Message):
    await message.answer(
        "Ввидеите название фильма, год, жанр, актёров или режисёров. Мы попытаемся найти соответствующий фильм",
            reply_markup=client_kb.cancel_kb)
    await SearchM.look.set()


@dp.message_handler(state=SearchM.look)
async def search_ans(message: types.Message, state: FSMContext):
    text = message.text.lower()
    text = movie_ganres_rus[text] if text in list(movie_ganres_rus.keys()) else message.text.lower()

    if text.lower() == "Отмена".lower():
        await message.answer("Поиск отменён ", reply_markup=client_kb.home_kb)
    else:
        movie_lst = await base.get_movie_search(text=text)
        print(movie_lst)
        if len(list(movie_lst)) == 0:
            await message.answer(f"По вашему запросу ничего не найденно", reply_markup=client_kb.home_kb)
        else:
            await message.answer("Список фильмов по вашему запросу", reply_markup=client_kb.home_kb)
            await message.answer("Выберите фильм из списка :", reply_markup=client_kb.search_kb(movie_lst, text))
    await state.finish()


@dp.callback_query_handler(Text(startswith="search_page"))
async def search_choose(callback: types.CallbackQuery):
    action = callback.data.split("_")[2]
    page = callback.data.split("_")[3]
    query = callback.data.split("_")[4]

    if action == "prev" and int(page) >= 2:
        movie_lst = await base.get_movie_search(query, int(page) - 1)
        await callback.message.edit_text("Выберите фильм из списка :",
                                         reply_markup=client_kb.search_kb(movie_lst, query, page=int(page) - 1))
    elif action == "next":
        movie_lst = await base.get_movie_search(query, int(page) + 1)
        await callback.message.edit_text("Выберите фильм из списка :",
                                         reply_markup=client_kb.search_kb(movie_lst, query, page=int(page) + 1))
    await callback.answer()


# Популярное ===========================================================================================================
async def popular(message: types.Message):
    pop = await base.get_movie_pop()
    await message.answer("Список самых популярных фильмов : ",
                         reply_markup=client_kb.pop_movies_kb(pop))


@dp.callback_query_handler(Text(startswith="show_pop"))
async def popular_show(callback: types.CallbackQuery):
    movie_id = callback.data.split("_")[2]
    await callback.message.delete()

    movie = await base.get_movie_id(movie_id)
    movie = dict(movie[0][0])

    ganre = movie_ganres[movie['ganre']]

    await callback.message.answer_video(movie["video"],
                                        caption=f"""<b>{movie['name']}</b>
        \n{movie['description']}
        \nЖанр: {ganre}\nГод: {movie['date']}\nСтрана: {movie['country']}
        \nРежисёр|Продюсер: {movie['producer']}\nАктёры: {movie['actors']}""",
                                        reply_markup=client_kb.like_kb(movie_id, movie["likes"]))


@dp.callback_query_handler(Text(startswith="like_movie"))
async def movie_like(callback: types.CallbackQuery):
    movie_id = callback.data.split("_")[2]
    user_id = callback.from_user.id
    # print(movie_id, user_id)
    await base.user_like_movie(user_id=user_id, movie_id=movie_id)
    await callback.message.edit_reply_markup(reply_markup=client_kb.before_liked)
    await callback.answer("Мы рады что фильм вам понравился 😊")


# Понравившиеся ========================================================================================================
async def liked(message: types.Message):
    movie = await base.get_movie_liked(message.from_user.id)
    await message.answer("Фильмы которые вам понравились: ", reply_markup=client_kb.liked_movies_kb(movie))


@dp.callback_query_handler(Text(startswith="show_liked"))
async def liked_show(callback: types.CallbackQuery):
    movie_id = callback.data.split("_")[2]
    await callback.message.delete()

    movie = await base.get_movie_id(movie_id)
    movie = dict(movie[0][0])

    ganre = movie_ganres[movie['ganre']]

    await callback.message.answer_video(movie["video"],
                                        caption=f"""<b>{movie['name']}</b>
        \n{movie['description']}
        \nЖанр: {ganre}\nГод: {movie['date']}\nСтрана: {movie['country']}
        \nРежисёр|Продюсер: {movie['producer']}\nАктёры: {movie['actors']}""", reply_markup=client_kb.before_liked)


async def about(message: types.Message):
    await message.answer("""Мы студенты СФИТ ТУИТ БГУИР
Кудайбергенов.А и Юнусов.У 
Данный бот является нашим курсовым проектов в 1 половине 3 курса. 
Основные функции это поиск и просмотр фильмов прямо в телеграмме не используя иные ресурсы. 
Такой метод удобен и универсален для любых устройств.""")


def register_client_handler(dp: Dispatcher):
    # Жанры
    dp.register_message_handler(genres, Text(startswith="Жанры", ignore_case=True))

    # Поиск
    dp.register_message_handler(search, Text(startswith="Поиск", ignore_case=True))

    # Популярное
    dp.register_message_handler(popular, Text(startswith="Популярное", ignore_case=True))

    # Понравившиеся
    dp.register_message_handler(liked, Text(startswith="Понравившиеся", ignore_case=True))

    # Про нас
    dp.register_message_handler(about, Text(startswith="Про нас", ignore_case=True))
