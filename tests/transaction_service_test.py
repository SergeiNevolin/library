import unittest
from unittest.mock import MagicMock
from services.transaction_service import TransactionService
from utils.date_validator import validate_date


class TestTransactionService(unittest.TestCase):

    def setUp(self):
        self.mock_db_manager = MagicMock()
        self.mock_book_service = MagicMock()
        self.mock_reader_service = MagicMock()

        self.transaction_service = TransactionService("mock_db_path")
        self.transaction_service.db_manager = self.mock_db_manager
        self.transaction_service.book_service = self.mock_book_service
        self.transaction_service.reader_service = self.mock_reader_service

    def test_add_transaction(self):
        book_id = 1
        reader_id = 1
        borrow_date = "2024-11-17"
        expected_return_date = "2024-11-24"
        return_date = None

        self.mock_db_manager.execute_query.return_value = None

        self.transaction_service.add_transaction(book_id, reader_id, borrow_date, expected_return_date, return_date)

        expected_query = """INSERT INTO transactions (book_id, reader_id, borrow_date, return_date, expected_return_date) VALUES (?, ?, ?, ?, ?)"""
        self.mock_db_manager.execute_query.assert_called_once_with(
            expected_query,
            (book_id, reader_id, borrow_date, return_date, expected_return_date)
        )


    def test_record_transaction_book_unavailable(self):
        book_id = 1
        reader_id = 1

        self.mock_book_service.is_book_available.return_value = False
        self.mock_book_service.get_or_create_book.return_value = book_id
        self.mock_reader_service.get_or_create_reader.return_value = reader_id

        # мок на ввод b
        with unittest.mock.patch('builtins.input', return_value='b'):
            self.transaction_service.record_transaction()

        self.mock_db_manager.execute_query.assert_not_called()

    def test_record_transaction_invalid_action(self):
        book_id = 1
        reader_id = 1

        self.mock_book_service.get_or_create_book.return_value = book_id
        self.mock_reader_service.get_or_create_reader.return_value = reader_id

        # мок на ввод x
        with unittest.mock.patch('builtins.input', return_value='x'):
            self.transaction_service.record_transaction()

        self.mock_db_manager.execute_query.assert_not_called()


if __name__ == '__main__':
    unittest.main()
