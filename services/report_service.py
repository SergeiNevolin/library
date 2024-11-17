from db.db_manager import DBManager
import os

class ReportService:
    def __init__(self, db_path):
        self.db_manager = DBManager(db_path)

    def available_books(self):
        """Сколько свободных книг есть в библиотеке на текущий момент."""
        query = """
        SELECT COUNT(*) AS available_books
        FROM books
        WHERE id NOT IN (
            SELECT book_id
            FROM transactions
            WHERE return_date IS NULL
        );
        """
        result = self.db_manager.fetch_all(query)
        return result[0][0] if result else 0


    def books_taken_by_each_reader(self):
        """Сколько книг брал каждый читатель за все время."""
        query = """
        SELECT readers.name, COUNT(transactions.book_id) AS books_taken
        FROM readers
        LEFT JOIN transactions ON readers.id = transactions.reader_id
        GROUP BY readers.id
        ORDER BY books_taken DESC;
        """
        result = self.db_manager.fetch_all(query)
        return result


    def books_with_each_reader(self):
        """Сколько книг сейчас находится на руках у каждого читателя."""
        query = """
        SELECT readers.name, COUNT(transactions.book_id) AS books_on_hand
        FROM readers
        LEFT JOIN transactions ON readers.id = transactions.reader_id
        WHERE transactions.return_date IS NULL
        GROUP BY readers.id
        ORDER BY books_on_hand DESC;
        """
        result = self.db_manager.fetch_all(query)
        return result

    def last_visit_date(self):
        """Дата последнего посещения читателем библиотеки."""
        query = """
        SELECT readers.name, MAX(transactions.borrow_date) AS last_visit
        FROM readers
        LEFT JOIN transactions ON readers.id = transactions.reader_id
        GROUP BY readers.id
        ORDER BY last_visit DESC;
        """
        result = self.db_manager.fetch_all(query)
        return result


    def popular_genres(self):
        """Наиболее предпочитаемые читателями жанры по убыванию."""
        query = """
        SELECT books.genre, COUNT(transactions.book_id) AS genre_count
        FROM books
        LEFT JOIN transactions ON books.id = transactions.book_id
        WHERE transactions.book_id IS NOT NULL
        GROUP BY books.genre
        ORDER BY genre_count DESC;
        """
        result = self.db_manager.fetch_all(query)
        return result

    def generate_overdue_report(self):
        """Сформировать отчет о всех просроченных книгах."""
        reports_folder = "reports"
        
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)

        query = """
        SELECT 
            readers.name AS reader_name, 
            books.title AS book_title, 
            transactions.expected_return_date AS expected_return_date
        FROM transactions
        JOIN books ON transactions.book_id = books.id
        JOIN readers ON transactions.reader_id = readers.id
        WHERE transactions.return_date IS NULL
        AND TRIM(transactions.expected_return_date) != ''
        AND transactions.expected_return_date < CURRENT_DATE;
        """
        
        overdue_books = self.db_manager.fetch_all(query)
        
        if not overdue_books:
            print("Нет просроченных книг.")
            return
        
        report_file = os.path.join(reports_folder, "overdue_books_report.txt")
        
        with open(report_file, "w") as file:
            file.write("Отчет о просроченных книгах\n")
            file.write("================================\n")
            for entry in overdue_books:
                reader_name, book_title, expected_return_date = entry
                file.write(f"Читатель: {reader_name}, Книга: {book_title}, Ожидаемая дата возврата: {expected_return_date}\n")
        
        print(f"Отчет о просроченных книгах сохранен в файл {report_file}.")

