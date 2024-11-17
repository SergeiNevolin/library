class AuthorService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_authors(self):
        """Получить список всех авторов."""
        query = "SELECT id, name FROM authors"
        return self.db_manager.fetch_all(query)

    def add_author(self, name):
        """Добавить нового автора в библиотеку."""
        query = "INSERT INTO authors (name) VALUES (?)"
        self.db_manager.execute_query(query, (name,))

    def display_authors(self, authors):
        """Отображает список авторов."""
        if authors:
            print("Список авторов:")
            for index, author in enumerate(authors, 1):
                print(f"{index}. {author[1]}")  # author[1] - имя автора
            return int(input("Выберите номер автора: ")) - 1
        else:
            print("Нет доступных авторов.")
            return -1
    
    def get_or_create_author(self):
        """Получить автора или создать нового."""
        authors = self.get_authors()
        if not authors:
            print("Авторы не зарегистрированы, добавьте автора.")
            return self.create_author()

        choice = input("Хотите выбрать существующего автора (1) или добавить нового (2)? ")
        if choice == '1':
            author_index = self.display_authors(authors)
            if author_index < 0 or author_index >= len(authors):
                print("Некорректный выбор.")
                return self.create_author()
            return authors[author_index][0]
        elif choice == '2':
            return self.create_author()
        else:
            print("Некорректный выбор. Попробуйте снова.")
            return self.get_or_create_author()

    def create_author(self):
        """Создать нового автора."""
        name = input("Введите имя автора: ")
        self.add_author(name)
        authors = self.get_authors()
        return authors[-1][0]