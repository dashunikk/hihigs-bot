from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button1 = InlineKeyboardButton(
    text="Я обожаю программирование!",
    callback_data="love_programming"  # Уникальный идентификатор
)
button2 = InlineKeyboardButton(
    text="НИ - мой любимый препод!",
    callback_data="favorite_teacher"
)
button3 = InlineKeyboardButton(
    text="Как можно жить без Python?",
    callback_data="life_without_python"
)

keyboards = InlineKeyboardMarkup(
    inline_keyboard=[  # Используем правильный параметр
        [button1],     # Первая строка с одной кнопкой
        [button2, button3]  # Вторая строка с двумя кнопками
    ],
    resize_keyboard=True,      # Автоматически подгонять размер
    one_time_keyboard=True     # Скрыть после нажатия
)