import unittest
from unittest.mock import MagicMock
from services.book_service import BookService


class TestBookService(unittest.TestCase):

    def setUp(self):
        self.mock_db_manager = MagicMock()
        self.book_service = BookService(self.mock_db_manager)

    def test_add_book(self):
        self.mock_db_manager.execute_query.return_value = None

        title = "Мастер и Маргарита"
        author_id = 1
        genre = "Роман"
        
        self.book_service.add_book(title, author_id, genre)
        
        self.mock_db_manager.execute_query.assert_called_once_with(
            "INSERT INTO books (title, author_id, genre) VALUES (?, ?, ?)", 
            (title, author_id, genre)
        )

    def test_remove_book(self):
        book_id = 1
        
        self.mock_db_manager.execute_query.return_value = None

        self.book_service.remove_book(book_id)

        self.mock_db_manager.execute_query.assert_called_once_with(
            "DELETE FROM books WHERE id = ?", 
            (book_id,)
        )

    def test_update_book(self):
        book_id = 1
        title = "Новая книга"
        author_id = 2
        genre = "Фантастика"

        self.mock_db_manager.execute_query.return_value = None
        self.book_service.update_book(book_id, title, author_id, genre)

        self.mock_db_manager.execute_query.assert_called_once_with(
            "UPDATE books SET title = ?, author_id = ?, genre = ? WHERE id = ?", 
            (title, author_id, genre, book_id)
        )

    def test_get_books(self):
        self.mock_db_manager.fetch_all.return_value = [(1, "1984"), (2, "Краткая история времени")]

        books = self.book_service.get_books()

        self.assertEqual(len(books), 2)
        self.assertEqual(books[0][1], "1984")
        self.assertEqual(books[1][1], "Краткая история времени")

    def test_is_book_available(self):
        book_id = 1
        self.mock_db_manager.fetch_all.return_value = [(0,)]

        available = self.book_service.is_book_available(book_id)
        self.assertTrue(available)

        self.mock_db_manager.fetch_all.return_value = [(1,)]

        available = self.book_service.is_book_available(book_id)
        self.assertFalse(available)

if __name__ == '__main__':
    unittest.main()
