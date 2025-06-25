from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Старые клавиатуры (оставляем без изменений)
button_continue = InlineKeyboardButton(text="Далее", callback_data="button_continue")
button_tutor = InlineKeyboardButton(text="Преподаватель", callback_data="button_tutor")
button_student = InlineKeyboardButton(text="Слушатель", callback_data="button_student")

keyboard_continue = InlineKeyboardMarkup(inline_keyboard=[[button_continue]])
keyboard_start = InlineKeyboardMarkup(inline_keyboard=[[button_tutor, button_student]])

# Новые клавиатуры для команд vmpath и check
# Кнопки для vmpath
button_save_vm = InlineKeyboardButton(text="Сохранить ВМ", callback_data="save_vm")
button_test_connection = InlineKeyboardButton(text="Проверить подключение", callback_data="test_connection")

# Кнопки для check
button_check_now = InlineKeyboardButton(text="Проверить сейчас", callback_data="check_now")
button_view_details = InlineKeyboardButton(text="Просмотреть данные", callback_data="view_details")

# Клавиатура для команды vmpath
keyboard_vmpath = InlineKeyboardMarkup(inline_keyboard=[
    [button_save_vm],
    [button_test_connection]
])

# Клавиатура для команды check
keyboard_check = InlineKeyboardMarkup(inline_keyboard=[
    [button_check_now],
    [button_view_details]
])