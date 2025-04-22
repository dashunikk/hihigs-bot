import os
from pathlib import Path
from dotenv import load_dotenv

# TODO костыль
parent = Path(f"{os.getcwd()}").parent


def test_logs_folder_exists():
    log_path = Path(f"{parent}/log")
    assert log_path.exists(), "Папка log/ не найдена"
    assert log_path.is_dir(), "log/ существует, но не является директорией"


def test_env_file_exists():
    env_path = Path(f"{parent}/.env")
    assert env_path.exists(), "Файл .env не найден"
    assert env_path.is_file(), ".env существует, но не является файлом"


def test_env_variable_loaded():
    load_dotenv()
    bot_token = os.getenv("TOKEN")
    assert bot_token, "TOKEN не найден в переменных окружения"