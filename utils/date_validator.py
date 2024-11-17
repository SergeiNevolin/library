from datetime import datetime

def validate_date(date_string):
    """Валидация и преобразование строки в объект даты (формат: YYYY-MM-DD)."""
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
        return date_obj
    except ValueError:
        print(f"Неверный формат даты: {date_string}. Пожалуйста, используйте формат YYYY-MM-DD.")
        return None

def get_valid_date(prompt):
    """Запрашивает дату у пользователя и проверяет её корректность.
    Повторяет запрос, если дата введена неверно."""
    while True:
        date_string = input(prompt)
        date_obj = validate_date(date_string)
        if date_obj:
            return date_obj
        print("Попробуйте снова.")