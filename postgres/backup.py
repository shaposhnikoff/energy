import os
import datetime
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Конфигурация
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
BACKUP_DIR = "./backups"

# Убедимся, что каталог существует
os.makedirs(BACKUP_DIR, exist_ok=True)

# Формируем имя файла
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_file = os.path.join(BACKUP_DIR, f"{DB_NAME}_{timestamp}.sql")

# Установка переменной окружения для пароля
env = os.environ.copy()
env["PGPASSWORD"] = DB_PASSWORD

# Команда pg_dump
cmd = [
    "pg_dump",
    "-h", DB_HOST,
    "-p", DB_PORT,
    "-U", DB_USER,
    "-d", DB_NAME,
    "-F", "p",  # plain SQL
    "-f", backup_file
]

try:
    subprocess.run(cmd, check=True, env=env)
    print(f"[✅] Backup successful: {backup_file}")
except subprocess.CalledProcessError as e:
    print(f"[❌] Backup failed: {e}")


