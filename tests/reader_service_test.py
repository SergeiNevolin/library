import unittest
from unittest.mock import MagicMock
from services.reader_service import ReaderService

class TestReaderService(unittest.TestCase):
    
    def setUp(self):
        self.mock_db_manager = MagicMock()
        self.reader_service = ReaderService(self.mock_db_manager)

    def test_get_readers(self):
        self.mock_db_manager.fetch_all.return_value = [(1, 'Иван Иванов', 59.9343, 30.3351)]
        
        readers = self.reader_service.get_readers()
        
        self.assertEqual(len(readers), 1)
        self.assertEqual(readers[0][1], 'Иван Иванов')

    def test_add_reader(self):
        self.reader_service.add_reader('Петр Петров', 'г. Москва, ул. Пушкина', 55.7558, 37.6176)
        
        self.mock_db_manager.execute_query.assert_called_with(
            "INSERT INTO readers (name, address, latitude, longitude) VALUES (?, ?, ?, ?)",
            ('Петр Петров', 'г. Москва, ул. Пушкина', 55.7558, 37.6176)
        )

    def test_remove_reader(self):
        self.reader_service.remove_reader(1)
        
        self.mock_db_manager.execute_query.assert_called_with(
            "DELETE FROM readers WHERE id = ?",
            (1,)
        )

    def test_update_reader(self):
        self.reader_service.update_reader(1, 'Иван Иванович', 'г. Пермь, ул. Ленина', 58.0173, 56.3200)
        
        self.mock_db_manager.execute_query.assert_called_with(
            "UPDATE readers SET name = ?, address = ?, latitude = ?, longitude = ? WHERE id = ?",
            ('Иван Иванович', 'г. Пермь, ул. Ленина', 58.0173, 56.3200, 1)
        )

if __name__ == "__main__":
    unittest.main()
