from services.author_service import AuthorService


class BookService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.author_service = AuthorService(self.db_manager)

    def get_books(self):
        """Получить все книги в библиотеке."""
        query = "SELECT id, title FROM books"
        return self.db_manager.fetch_all(query)

    def add_book(self, title, author_id, genre):
        """Добавить новую книгу в библиотеку."""
        query = "INSERT INTO books (title, author_id, genre) VALUES (?, ?, ?)"
        params = (title, author_id, genre)
        self.db_manager.execute_query(query, params)

    def remove_book(self, book_id):
        """Удалить книгу из библиотеки."""
        query = "DELETE FROM books WHERE id = ?"
        params = (book_id,)
        self.db_manager.execute_query(query, params)
        print("Книга успешно удалена!")

    def update_book(self, book_id, title=None, author_id=None, genre=None):
        """Обновить данные о книге."""
        query = "UPDATE books SET title = ?, author_id = ?, genre = ? WHERE id = ?"
        params = (title, author_id, genre, book_id)
        self.db_manager.execute_query(query, params)
        print("Данные о книге успешно обновлены!")

    def display_books(self, books):
        """Отображает список книг."""
        if books:
            print("Список книг:")
            for index, book in enumerate(books, 1):
                print(f"{index}. {book[1]}")  # book[1] - название книги
            return int(input("Выберите номер книги: ")) - 1
        else:
            print("Нет доступных книг.")
            return -1

    def get_or_create_book(self):
        """Получить книгу или создать новую."""
        books = self.get_books()
        if not books:
            print("Книги в библиотеке нет, добавьте книгу.")
            return self.create_book()

        choice = input("Хотите выбрать существующую книгу (1) или добавить новую (2)? ")
        if choice == '1':
            book_index = self.display_books(books)
            if book_index < 0 or book_index >= len(books):
                print("Некорректный выбор.")
                return self.create_book()
            return books[book_index][0]
        elif choice == '2':
            return self.create_book()
        else:
            print("Некорректный выбор. Попробуйте снова.")
            return self.get_or_create_book()

    def create_book(self):
        """Создать новую книгу."""
        title = input("Введите название книги: ")
        author_id = self.author_service.get_or_create_author()
        genre = input("Введите жанр книги: ")
        self.add_book(title, author_id, genre)
        books = self.get_books()
        return books[-1][0]
    
    
    def is_book_available(self, book_id):
        """Проверить, доступна ли книга для взятия."""
        query = """
        SELECT COUNT(*) FROM transactions
        WHERE book_id = ? AND return_date IS NULL
        """
        result = self.db_manager.fetch_all(query, (book_id,))
        return result[0][0] == 0  # Если возвращаемое количество равно 0, книга доступна