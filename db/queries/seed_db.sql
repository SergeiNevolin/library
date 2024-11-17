-- Добавление данных в таблицы SQLite

-- Авторы
INSERT INTO authors (name) VALUES 
('Достоевский Ф.М.'),
('Пушкин А.С.'),
('Толстой Л.Н.');

-- Книги
INSERT INTO books (title, author_id, genre) VALUES 
('Преступление и наказание', 1, 'Роман'),
('Евгений Онегин', 2, 'Поэма'),
('Война и мир', 3, 'Роман');

-- Читатели
INSERT INTO readers (name, address, latitude, longitude) VALUES 
('Иван Иванов', 'г. Пермь, ул. Ленина, д. 10', 58.0100, 56.2500),
('Мария Петрова', 'г. Пермь, ул. Космонавтов, д. 15', 58.0250, 56.2670);

-- Транзакции
INSERT INTO transactions (book_id, reader_id, borrow_date, expected_return_date) VALUES 
(1, 1, '2024-11-01', '2024-11-15'),
(3, 1, '2024-11-01', '2024-11-15'),
(2, 2, '2024-11-05', '2024-11-19');
