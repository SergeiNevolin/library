from db.db_setup import DBSetup
from services.geo_report_service import GeoReportService
from services.transaction_service import TransactionService
from services.report_service import ReportService
from utils.menu import Menu

def main():
    db_path = "library.db"

    # Инициализация базы данных
    setup = DBSetup(db_path)
    setup.initialize(seed_data=True)

    # Создание сервисов
    transaction_service = TransactionService(db_path)
    report_service = ReportService(db_path)
    geo_report_service = GeoReportService(db_path)

    # Инициализация меню
    menu = Menu(transaction_service, report_service, geo_report_service)

    running = True
    while running:
        menu.display_menu()
        choice = input("Выберите действие: ")
        running = menu.handle_choice(choice)

if __name__ == "__main__":
    main()
