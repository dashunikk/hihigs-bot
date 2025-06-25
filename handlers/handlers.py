from aiogram import types, Router, filters, F, Dispatcher
from sqlalchemy import select
from db import async_session, User
from .keyboard import keyboard_continue, keyboard_start, keyboard_vmpath, keyboard_check  # добавлены новые клавиатуры
from .callbacks import callback_message, callback_start_tutor, callback_insert_tutorcode, start_student
from script.classes import VMConnect
from script.db import save_user, get_user_role
from script.db import get_vm_data, save_vm_data  # Добавляем импорт нужных функций

# информация о статусе
status_string: str = """
UserId: {}
UserName: {}
"""

async def process_help_command(message):
    """Команда help"""
    await message.answer("Помоги!", reply_markup=keyboard_continue)

async def process_start_command(message: types.Message):
    """Команда регистрации и справки"""
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        result = await session.execute(query)
        if result.scalars().all():
            info = "Чтобы продолжить, вызовите команду /status"
            await message.answer(info)
        else:
            await message.answer("Выберите роль", reply_markup=keyboard_start)

async def process_status_command(message: types.Message):
    """Команда регистрации и справки"""
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        result = await session.execute(query)
        user = result.scalar()
        if user.tutorcode:
            info = status_string + "Код преподавателя: {}"
            info = info.format(user.user_id, user.username, user.tutorcode)
        if user.subscribe:
            code = str(user.subscribe)
            info = status_string + "Преподаватель: {}"
            query = select(User).where(code == User.tutorcode)
            result = await session.execute(query)
            tutor = result.scalar()
            try:
                info = info.format(user.user_id, user.username, tutor.username)
            except:
                info = info.format(user.user_id, user.username)
        await message.answer(info)


async def vmpath_command(message: types.Message):
    """Обработчик команды /vmpath"""
    try:
        parts = message.text.split()
        if len(parts) != 4:
            await message.answer(
                "Используйте: /vmpath <ip> <username> <password>",
                reply_markup=keyboard_vmpath
            )
            return

        ip, username, password = parts[1], parts[2], parts[3]
        save_vm_data(message.from_user.id, ip, username, password)  # Сохраняем данные ВМ

        vm = VMConnect(address=ip, username=username, password=password)
        if vm.connect():
            await message.answer(
                f"Данные ВМ сохранены. Подключение успешно: {ip}",
                reply_markup=keyboard_vmpath
            )
        else:
            await message.answer(
                "Ошибка подключения к ВМ. Данные сохранены, но подключение не удалось.",
                reply_markup=keyboard_vmpath
            )
    except Exception as e:
        await message.answer(
            f"Ошибка: {str(e)}",
            reply_markup=keyboard_vmpath
        )


async def check_command(message: types.Message):
    """Обработчик команды /check"""
    try:
        vm_data = get_vm_data(message.from_user.id)  # Получаем сохранённые данные VM
        if not vm_data:
            await message.answer(
                "Сначала укажите данные ВМ через /vmpath.",
                reply_markup=keyboard_check
            )
            return

        ip, username, password = vm_data
        vm = VMConnect(address=ip, username=username, password=password)

        if vm.connect():
            await message.answer(
                "Подключение к ВМ успешно!",
                reply_markup=keyboard_check
            )
        else:
            await message.answer(
                "Не удалось подключиться к ВМ.",
                reply_markup=keyboard_check
            )
    except Exception as e:
        await message.answer(
            f"Ошибка: {str(e)}",
            reply_markup=keyboard_check
        )

async def ls_command(message: types.Message):
    """Обработчик команды /ls"""
    try:
        vm_data = get_vm_data(message.from_user.id)
        if not vm_data:
            await message.answer("Сначала укажите данные ВМ через /vmpath.")
            return

        vm = VMConnect(*vm_data)
        if vm.connect():
            files = vm.list_files()
            await message.answer(f"Файлы в домашней директории:\n{files}")
        else:
            await message.answer("Не удалось подключиться к ВМ.")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

async def cat_command(message: types.Message):
    """Обработчик команды /cat"""
    try:
        vm_data = get_vm_data(message.from_user.id)
        if not vm_data:
            await message.answer("Сначала укажите данные ВМ через /vmpath.")
            return

        vm = VMConnect(*vm_data)
        if vm.connect():
            files = vm.list_files().split()
            for filename in files:
                if filename.endswith('.txt'):
                    content = vm.read_file(filename)
                    await message.answer(f"Содержимое {filename}:\n{content}")
        else:
            await message.answer("Не удалось подключиться к ВМ.")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

async def register_message_handlers(router: Router):
    """Маршрутизация обработчиков"""
    router.message.register(process_start_command, filters.Command(commands=["start"]))
    router.message.register(process_status_command, filters.Command(commands=["status"]))
    router.message.register(vmpath_command, filters.Command(commands=["vmpath"]))
    router.message.register(check_command, filters.Command(commands=["check"]))
    router.callback_query.register(callback_message, F.data.endswith("_continue"))
    router.callback_query.register(callback_start_tutor, F.data.endswith("_tutor"))
    router.callback_query.register(callback_insert_tutorcode, F.data.endswith("_student"))
    router.message.register(start_student, F.text.startswith("tutorcode-"))
    router.message.register(ls_command, filters.Command(commands=["ls"]))
    router.message.register(cat_command, filters.Command(commands=["cat"]))