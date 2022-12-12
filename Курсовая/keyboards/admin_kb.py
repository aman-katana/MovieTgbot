from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_btn = KeyboardButton("Назад ⬅")
back_admin = KeyboardButton("Обратно 🔙")

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_1 = KeyboardButton("Загрузить")
admin_2 = KeyboardButton("Удалить")
admin_3 = KeyboardButton("Данные")
admin_4 = KeyboardButton("Кнопка 4")
admin_5 = KeyboardButton("Кнопка 5")
admin_6 = KeyboardButton("Кнопка 6")
admin_kb.add(admin_1, admin_2).add(back_btn)

stop_load = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="Остановить загрузку", callback_data="stop_load")
)

ganre_kb = InlineKeyboardMarkup(row_width=2)
ganre_1 = InlineKeyboardButton(text="Комедия", callback_data="ganre_comedy")
ganre_2 = InlineKeyboardButton(text="Фантастика", callback_data="ganre_fantasy")
ganre_3 = InlineKeyboardButton(text="Ужасы", callback_data="ganre_horror")
ganre_4 = InlineKeyboardButton(text="Боевик", callback_data="ganre_action")
ganre_5 = InlineKeyboardButton(text="Мелодрама", callback_data="ganre_melodrama")
ganre_6 = InlineKeyboardButton(text="Мистика", callback_data="ganre_mystic")
ganre_7 = InlineKeyboardButton(text="Детектив", callback_data="ganre_detective")
ganre_8 = InlineKeyboardButton(text="Военное", callback_data="ganre_military")
ganre_kb.add(ganre_1, ganre_2, ganre_3, ganre_4, ganre_5, ganre_6, ganre_7, ganre_8)


confirm_kb = ReplyKeyboardMarkup(resize_keyboard=True)
confirm_1 = KeyboardButton("Подтвердить")
confirm_2 = KeyboardButton("Отменить загрузку")
confirm_kb.add(confirm_1).add(confirm_2)
