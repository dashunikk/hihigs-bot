import sqlite3

def get_db_connection():
    """Создаёт и возвращает подключение к базе данных"""
    conn = sqlite3.connect('vm_data.db')
    return conn

async def save_user(user_id: int, username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

async def get_user_role(user_id: int) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    role = cursor.fetchone()[0]  # Предполагается, что роль хранится в столбце 'role'
    conn.close()
    return role or "student"  # По умолчанию роль 'student'