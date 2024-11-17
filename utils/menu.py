class Menu:
    def __init__(self, transaction_service, report_service, geo_report_service):
        """
        Инициализирует меню с необходимыми сервисами.
        """
        self.transaction_service = transaction_service
        self.report_service = report_service
        self.geo_report_service = geo_report_service

    def display_menu(self):
        """
        Отображает меню пользователю.
        """
        print("\nМеню:")
        print("1. Добавить факт взятия/возврата книги")
        print("2. Просмотреть отчеты")
        print("q. Выйти")

    def handle_choice(self, choice):
        """
        Обрабатывает выбор пользователя.
        """
        if choice == "1":
            self.transaction_service.record_transaction()
        elif choice == "2":
            self.display_reports()
        elif choice == "q":
            print("До свидания!")
            return False
        else:
            print("Неверный выбор, попробуйте снова.")
        return True

    def display_reports(self):
        """Меню для отображения отчетов."""
        while True:
            print("\nВыберите отчет:")
            print("1. Сколько свободных книг есть в библиотеке на текущий момент")
            print("2. Сколько книг брал каждый читатель за все время")
            print("3. Сколько книг сейчас находится на руках у каждого читателя")
            print("4. Дата последнего посещения читателем библиотеки")
            print("5. Наиболее предпочитаемые читателями жанры по убыванию")
            print("6. Сформировать отчет о всех просроченных книгах")
            print("7. Сформировать отчет о расположении читателей и выданных книгах в формате GeoJSON")
            print("q. Вернуться в главное меню")

            choice = input("Введите номер отчета (или 'q' для выхода): ")

            if choice == "1":
                count = self.report_service.available_books()
                print(f"\nСвободных книг в библиотеке: {count}")
            elif choice == "2":
                data = self.report_service.books_taken_by_each_reader()
                print("\nСколько книг брал каждый читатель:")
                for name, count in data:
                    print(f"{name}: {count} книг")
            elif choice == "3":
                data = self.report_service.books_with_each_reader()
                print("\nСколько книг сейчас находится на руках:")
                for name, count in data:
                    print(f"{name}: {count} книг")
            elif choice == "4":
                data = self.report_service.last_visit_date()
                print("\nДата последнего посещения читателями:")
                for name, date in data:
                    print(f"{name}: {date}")
            elif choice == "5":
                data = self.report_service.popular_genres()
                print("\nНаиболее предпочитаемые жанры:")
                for genre, count in data:
                    print(f"{genre}: {count} взятий")
            elif choice == "6":
                self.report_service.generate_overdue_report()
            elif choice == "7":
                self.geo_report_service.generate_geojson_report()
            elif choice.lower() == "q":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
