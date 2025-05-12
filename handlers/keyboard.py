from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#Inline-кнопка "Далее"
#Inline-кнопка "Слушатель"
#Inline-кнопка "Преподаватель"

button_continue = InlineKeyboardButton(text="Далее", callback_data="button_continue")
button_tutor = InlineKeyboardButton(text="Преподаватель", callback_data="button_tutor")
button_student = InlineKeyboardButton(text="Слушатель", callback_data="button_student")

#Inline-клавиатура "Продолжить"
keyboard_continue = InlineKeyboardMarkup(inline_keyboard=[
        [button_continue, ]
    ])

#Inline-клавиатура "Выберите роль"
keyboard_start = InlineKeyboardMarkup(inline_keyboard=[
        [button_tutor, button_student]
    ])
