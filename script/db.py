import sqlite3

def get_db_connection():
    """Создаёт и возвращает подключение к базе данных"""
    conn = sqlite3.connect('vm_data.db')
    return conn

def init_db():
    """Создаёт таблицу vm_commands, если она не существует"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vm_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            output TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_command(conn, command, output):
    """Сохраняет команду и её результат в базу данных"""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vm_commands (command, output)
        VALUES (?, ?)
    ''', (command, output))
    conn.commit()