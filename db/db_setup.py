import os
import sqlite3

class DBSetup:
    def __init__(self, db_path="library.db", create_script="db/queries/create_db.sql", seed_script="db/queries/seed_db.sql"):
        self.db_path = db_path
        self.create_script = create_script
        self.seed_script = seed_script

    def execute_script(self, script_path):
        """Выполняет SQL-скрипт из файла."""
        with open(script_path, "r", encoding="utf-8") as file:
            sql_script = file.read()
        
        # Подключение к базе данных
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.executescript(sql_script)  # Выполняем весь скрипт
            conn.commit()
            print(f"Скрипт {script_path} выполнен успешно.")
        except sqlite3.OperationalError as e:
            print(f"Ошибка выполнения скрипта {script_path}: {e}")
        finally:
            conn.close()

    def initialize(self, seed_data=False):
        """Инициализирует базу данных."""
        if os.path.exists(self.db_path):
            print(f"База данных {self.db_path} уже существует.")
            return

        print("Создаю базу данных...")
        self.execute_script(self.create_script)
        print("База данных создана.")

        if seed_data:
            print("Заполняю тестовыми данными...")
            self.execute_script(self.seed_script)
            print("База данных успешно заполнена.")
