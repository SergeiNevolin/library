def get_valid_coordinate(prompt, min_value, max_value):
    """Запрашивает координату и проверяет её корректность."""
    while True:
        coordinate = input(prompt)
        if coordinate:
            try:
                coordinate = float(coordinate)
                if min_value <= coordinate <= max_value:
                    return coordinate
                else:
                    print(f"Ошибка: координата должна быть в пределах от {min_value} до {max_value}. Попробуйте снова.")
            except ValueError:
                print("Ошибка: введено не число. Попробуйте снова.")
        else:
            return None