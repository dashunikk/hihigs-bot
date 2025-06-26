__all__ = [
    "register_message_handlers",
]

from aiogram import types, Router, filters, F
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
import logging

from db import async_session
from db.models import User  # Изменение: импорт User из db.models вместо db
from .keyboard import keyboard_continue, keyboard_start
from .callbacks import (
    callback_message,
    callback_start_tutor,
    callback_insert_tutorcode,
    start_student
)
from script.classes import VMConnect

router = Router()

# информация о статусе
status_string: str = """
UserId: {}
UserName: {}
Вызовите команду /vmpath для указания адреса виртуальной машины 
"""


async def process_help_command(message):
    """Команда help"""
    await message.answer("Помоги!", reply_markup=keyboard_continue)


async def process_start_command(message: types.Message):
    """Команда регистрации и справки"""
    async with async_session() as session:
        logging.info(f"Checking user in DB: {message.from_user.id}")
        # Изменение: используем User.user_id вместо message.from_user.id в where
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()  # Изменение: используем scalar() вместо scalars().all()
        logging.info(f"Query result: {user}")

        if user:
            info = "Чтобы продолжить, вызовите команду /status"
            await message.answer(info)
        else:
            await message.answer("Выберите роль", reply_markup=keyboard_start)


async def process_status_command(message: types.Message):
    """Команда регистрации и справки"""
    async with async_session() as session:
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()

        if not user:
            await message.answer("Сначала зарегистрируйтесь через /start")
            return

        info = status_string.format(user.user_id, user.username)

        if user.tutorcode:
            info += f"Код преподавателя: {user.tutorcode}"

        elif user.subscribe:
            query = select(User).where(User.tutorcode == user.subscribe)
            tutor = (await session.execute(query)).scalar()
            if tutor:
                info += f"Преподаватель: {tutor.username}"

        await message.answer(info)


async def vmpath_command(message: types.Message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            await message.answer("Используйте: /vmpath <ip> <username> <password>")
            return

        async with async_session() as session:
            user = await session.get(User, message.from_user.id)

            if user:
                stmt = (
                    update(User)
                    .where(User.user_id == message.from_user.id)
                    .values(
                        vm_ip=parts[1],
                        vm_username=parts[2],
                        vm_password=parts[3]
                    )
                )
                await session.execute(stmt)
            else:

                user = User(
                    user_id=message.from_user.id,
                    username=message.from_user.username,
                    vm_ip=parts[1],
                    vm_username=parts[2],
                    vm_password=parts[3]
                )
                session.add(user)

            await session.commit()
            await message.answer(f"Данные ВМ сохранены: {parts[1]}")

    except SQLAlchemyError as e:
        await message.answer(f"Ошибка базы данных: {str(e)}")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


async def check_command(message: types.Message):
    try:
        async with async_session() as session:
            user = await session.get(User, message.from_user.id)
            if not user or not user.vm_ip:
                await message.answer("Сначала укажите данные ВМ через /vmpath.")
                return

            vm = VMConnect(
                address=user.vm_ip,
                username=user.vm_username,
                password=user.vm_password
            )

            if vm.check_connection():
                await message.answer("Подключение к ВМ активно.")
            else:
                await message.answer("Подключение к ВМ неактивно.")

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


async def ls_command(message: types.Message):
    try:
        async with async_session() as session:
            user = await session.get(User, message.from_user.id)
            if not user or not user.vm_ip:
                await message.answer("Сначала укажите данные ВМ через /vmpath.")
                return

            vm = VMConnect(
                address=user.vm_ip,
                username=user.vm_username,
                password=user.vm_password
            )

            if vm.connect():
                files = vm.list_files()
                await message.answer(f"Файлы в домашней директории:\n{files}")
            else:
                await message.answer("Не удалось подключиться к ВМ.")

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


async def cat_command(message: types.Message):
    try:
        async with async_session() as session:
            user = await session.get(User, message.from_user.id)
            if not user or not user.vm_ip:
                await message.answer("Сначала укажите данные ВМ через /vmpath.")
                return

            vm = VMConnect(
                address=user.vm_ip,
                username=user.vm_username,
                password=user.vm_password
            )

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
    router.message.register(ls_command, filters.Command(commands=["ls"]))
    router.message.register(cat_command, filters.Command(commands=["cat"]))
    router.callback_query.register(callback_message, F.data.endswith("_continue"))
    router.callback_query.register(callback_start_tutor, F.data.endswith("_tutor"))
    router.callback_query.register(callback_insert_tutorcode, F.data.endswith("_student"))
    router.message.register(start_student, F.text.startswith("tutorcode-"))