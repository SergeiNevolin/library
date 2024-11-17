import sqlite3

class DBManager:
    def __init__(self, db_path="library.db"):
        self.db_path = db_path

    def connect(self):
        """Создает соединение с базой данных."""
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=None):
        """Выполняет запрос к базе данных."""
        conn = self.connect()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()

    def fetch_all(self, query, params=None):
        """Выполняет SELECT-запрос и возвращает все результаты."""
        conn = self.connect()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
