from utils.coordinate_validator import get_valid_coordinate


class ReaderService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_readers(self):
        """Получить всех читателей библиотеки."""
        query = "SELECT id, name, latitude, longitude FROM readers"
        return self.db_manager.fetch_all(query)

    def add_reader(self, name, address, latitude=None, longitude=None):
        """Добавить нового читателя в библиотеку, включая информацию о местоположении."""
        query = "INSERT INTO readers (name, address, latitude, longitude) VALUES (?, ?, ?, ?)"
        params = (name, address, latitude, longitude)
        self.db_manager.execute_query(query, params)

    def display_readers(self, readers):
        """Отображает список читателей."""
        if readers:
            print("Список читателей:")
            for index, reader in enumerate(readers, 1):
                print(f"{index}. {reader[1]}")  # reader[1] - имя читателя
            return int(input("Выберите номер читателя: ")) - 1
        else:
            print("Нет доступных читателей.")
            return -1
        
    def choose_reader(self, readers):
        reader_index = self.display_readers(readers)
        if reader_index < 0 or reader_index >= len(readers):
            print("Некорректный выбор.")
            return None

        return reader_index

    def get_or_create_reader(self):
        """Получить читателя или создать нового."""
        readers = self.get_readers()
        if not readers:
            print("Читатели не зарегистрированы, добавьте читателя.")
            return self.create_reader()

        choice = input("Хотите выбрать существующего читателя (1) или добавить нового (2)? ")
        if choice == '1':
            reader_index = self.choose_reader(readers)
            if not reader_index:
                return self.create_reader()
            return readers[reader_index][0]
        elif choice == '2':
            return self.create_reader()
        else:
            print("Некорректный выбор. Попробуйте снова.")
            return self.get_or_create_reader()

    def create_reader(self):
        """Создать нового читателя."""
        name = input("Введите имя читателя: ")
        address = input("Введите адрес читателя: ")

        latitude = get_valid_coordinate("Введите широту читателя (или оставьте пустым): ", -90, 90)
        longitude = get_valid_coordinate("Введите долготу читателя (или оставьте пустым): ", -180, 180)

        self.add_reader(name, address, latitude, longitude)
        readers = self.get_readers() 
        return readers[-1][0] 
    
    def remove_reader(self, reader_id):
        """Удалить читателя из библиотеки."""
        query = "DELETE FROM readers WHERE id = ?"
        params = (reader_id,)
        self.db_manager.execute_query(query, params)
        print("Читатель успешно удален!")

    def update_reader(self, reader_id, name=None, address=None, latitude=None, longitude=None):
        """Обновить данные о читателе."""
        query = "UPDATE readers SET name = ?, address = ?, latitude = ?, longitude = ? WHERE id = ?"
        params = (name, address, latitude, longitude, reader_id)
        self.db_manager.execute_query(query, params)
        print("Данные о читателе успешно обновлены!")
