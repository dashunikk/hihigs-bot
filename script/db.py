import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Создаёт подключение к базе данных"""
    conn = sqlite3.connect('vm_bot.db')
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Инициализирует базу данных"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                tutorcode TEXT,
                subscribe TEXT
            )
        ''')
        # Таблица данных VM
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vm_connections (
                user_id INTEGER PRIMARY KEY,
                vm_address TEXT,
                vm_username TEXT,
                vm_password TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        conn.commit()

def save_user(user_id: int, username: str, tutorcode=None, subscribe=None):
    """Сохраняет пользователя"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, tutorcode, subscribe)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, tutorcode, subscribe))
        conn.commit()

def save_vm_data(user_id: int, address: str, username: str, password: str):
    """Сохраняет данные VM"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO vm_connections (user_id, vm_address, vm_username, vm_password)
            VALUES (?, ?, ?, ?)
        ''', (user_id, address, username, password))
        conn.commit()

def get_vm_data(user_id: int):
    """Получает данные VM"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT vm_address, vm_username, vm_password 
            FROM vm_connections 
            WHERE user_id = ?
        ''', (user_id,))
        return cursor.fetchone()

def get_user_role(user_id: int):
    """Получает роль пользователя"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT tutorcode, subscribe FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()