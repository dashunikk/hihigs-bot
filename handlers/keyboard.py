from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Создаём кнопки
button1 = KeyboardButton(text="Я обожаю программирование!")
button2 = KeyboardButton(text="НИ - мой любимый препод!")  # Новая кнопка 1
button3 = KeyboardButton(text="Как можно жить без Python?")  # Новая кнопка 2

# Создаём клавиатуру (добавляем кнопки в виде списка списков)
keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [button1],       # Первая строка с одной кнопкой
        [button2, button3]  # Вторая строка с двумя кнопками
    ],
    resize_keyboard=True,      # Автоматически подгонять размер
    one_time_keyboard=True     # Скрыть после нажатия
)
