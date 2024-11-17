# Создание виртуального окружения
venv:
	python -m venv venv

# Установка зависимостей
install:
	venv\Scripts\pip.exe install -r requirements.txt

# Создание базы данных
setup-db:
	venv\Scripts\python.exe db/setup_db.py

# Запуск приложения
run:
	venv\Scripts\python.exe app.py

# Удаление базы данных
clean-db:
	rm -f library.db
