from db.db_manager import DBManager
from services.book_service import BookService
from services.reader_service import ReaderService
from utils.date_validator import get_valid_date, validate_date

class TransactionService:
    def __init__(self, db_path):
        self.db_manager = DBManager(db_path)
        self.book_service = BookService(self.db_manager)
        self.reader_service = ReaderService(self.db_manager)

    def add_transaction(self, book_id, reader_id, borrow_date, expected_return_date=None, return_date=None):
        """Добавить факт взятия или возврата книги."""
        query = """INSERT INTO transactions (book_id, reader_id, borrow_date, return_date, expected_return_date) VALUES (?, ?, ?, ?, ?)"""
        params = (book_id, reader_id, borrow_date, return_date, expected_return_date)
        self.db_manager.execute_query(query, params)
        print("Транзакция добавлена успешно!")

    def record_transaction(self):
        """Запись факта взятия/возврата книги."""
        book_id = self.book_service.get_or_create_book()
        reader_id = self.reader_service.get_or_create_reader()

        action = input("Это взятие (b) или возврат (r)? ").strip().lower()

        if action == 'b':
            if not self.book_service.is_book_available(book_id):
                print("Эта книга уже взята и еще не возвращена.")
                return

            borrow_date = get_valid_date("Введите дату взятия (формат: YYYY-MM-DD): ")
            expected_return_date = input("Введите ожидаемую дату возврата (формат: YYYY-MM-DD, или оставьте пустым): ")
            if expected_return_date:
                expected_return_date = validate_date(expected_return_date)
                if expected_return_date is None:
                    return
            self.add_transaction(book_id, reader_id, borrow_date, expected_return_date)
        elif action == 'r':
            return_date = get_valid_date("Введите дату возврата (формат: YYYY-MM-DD): ")
            self.add_transaction(book_id, reader_id, "", return_date)
        else:
            print("Неверный выбор действия. Используйте 'b' для взятия или 'r' для возврата.")
