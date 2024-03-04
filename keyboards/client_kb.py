from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_btn = KeyboardButton("Назад ⬅")

home_kb = ReplyKeyboardMarkup(resize_keyboard=True)
home_1 = KeyboardButton(text="Жанры 🎥")
home_2 = KeyboardButton(text="Поиск 🔍")
home_3 = KeyboardButton(text="Популярное 🔝")
home_4 = KeyboardButton(text="Понравившиеся ❤")
home_5 = KeyboardButton(text="Про нас ❓")
home_kb.add(home_1, home_2).add(home_3, home_4).add(home_5)

choose_kb = InlineKeyboardMarkup(row_width=2)
ch_1 = InlineKeyboardButton(text="Комедия 😂", callback_data="choose_comedy")
ch_2 = InlineKeyboardButton(text="Фантастика 🤖", callback_data="choose_fantasy")
ch_3 = InlineKeyboardButton(text="Ужасы 👻", callback_data="choose_horror")
ch_4 = InlineKeyboardButton(text="Боевик 🔫", callback_data="choose_action")
ch_5 = InlineKeyboardButton(text="Мелодрама 😢", callback_data="choose_melodrama")
ch_6 = InlineKeyboardButton(text="Мистика 👽", callback_data="choose_mystic")
ch_7 = InlineKeyboardButton(text="Детектив 🕵", callback_data="choose_detective")
ch_8 = InlineKeyboardButton(text="Военное 🥷", callback_data="choose_military")
ch_stop = InlineKeyboardButton(text="Отмена ❌", callback_data="choose_stop")
choose_kb.add(ch_1, ch_2, ch_3, ch_4, ch_5, ch_6, ch_7, ch_8).add(ch_stop)


def movies_kb(info, genre, page=1):
    movie_btn = InlineKeyboardMarkup(row_width=3)
    for i in list(info):
        movie_id = i[0]
        d = dict(i[1])
        movie_btn.add(InlineKeyboardButton(text=f"{d['name']}", callback_data=f"show_movie_{movie_id}"))

    prv = InlineKeyboardButton(text=f"⏪", callback_data=f"genre_page_prev_{page}_{genre}")
    now = InlineKeyboardButton(text=f"{page} страница", callback_data=f"111")
    nex = InlineKeyboardButton(text="⏩", callback_data=f"genre_page_next_{page}_{genre}")
    back = InlineKeyboardButton(text="Назад ↖", callback_data=f"genre_page_back_{page}_{genre}")

    if page == 1 and len(list(info)) < 10:
        pass
    elif len(list(info)) < 10:
        movie_btn.add(prv, now)
    else:
        movie_btn.add(prv, now, nex)

    return movie_btn.add(back)


cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(
    text="Отмена"
))


def search_kb(info, query, page=1):
    search_btn = InlineKeyboardMarkup(row_width=3)
    for i in list(info):
        movie_id = i[0]
        d = dict(i[1])
        search_btn.add(InlineKeyboardButton(text=f"{d['name']}", callback_data=f"show_movie_{movie_id}"))

    prv = InlineKeyboardButton(text=f"⏪", callback_data=f"search_page_prev_{page}_{query}")
    now = InlineKeyboardButton(text=f"{page} страница", callback_data=f"111")
    nex = InlineKeyboardButton(text="⏩", callback_data=f"search_page_next_{page}_{query}")

    if page == 1 and len(list(info)) < 10:
        pass
    elif len(list(info)) < 10:
        search_btn.add(prv, now)
    else:
        search_btn.add(prv, now, nex)

    return search_btn


def pop_movies_kb(info):
    movie_btn = InlineKeyboardMarkup(row_width=3)
    for i in list(info):
        movie_id = i[0]
        d = dict(i[1])
        movie_btn.add(InlineKeyboardButton(text=f"{d['name']}", callback_data=f"show_pop_{movie_id}"))

    return movie_btn


def liked_movies_kb(info):
    movie_btn = InlineKeyboardMarkup(row_width=3)
    for i in list(info):
        movie_id = i[0]
        d = dict(i[1])
        movie_btn.add(InlineKeyboardButton(text=f"{d['name']}", callback_data=f"show_liked_{movie_id}"))

    return movie_btn


before_liked = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="Фильм вам понравился 😊", callback_data="111")
)


def like_kb(movie_id, likes):
    like_btn = InlineKeyboardMarkup(row_width=1)
    like_btn.add(InlineKeyboardButton(text=f"❤ {likes}", callback_data=f"like_movie_{movie_id}"))
    return like_btn
