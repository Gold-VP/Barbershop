# Импорт необходимых компонентов из Flask
from flask import Flask, render_template, request, redirect, url_for
# Импорт модуля для работы с базой данных SQLite
import sqlite3

# Создание экземпляра Flask приложения
app = Flask(__name__)

# Функция для инициализации базы данных
def init_db():
    # Установка соединения с базой данных (файл database.db)
    conn = sqlite3.connect('database.db')
    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()
    # Выполнение SQL-запроса для создания таблицы appointments, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY,         # Уникальный идентификатор записи
            client_name TEXT,               # Имя клиента
            date TEXT,                      # Дата записи
            time TEXT,                      # Время записи
            status TEXT DEFAULT 'pending'   # Статус записи (по умолчанию "ожидает")
        )
    ''')
    # Фиксация изменений в базе данных
    conn.commit()
    # Закрытие соединения с базой данных
    conn.close()

# Вызов функции инициализации базы данных при запуске приложения
init_db()

# Декоратор для корневой страницы ("/")
@app.route('/')
def index():
    # Отображение HTML-шаблона client.html
    return render_template('client.html')

# Декоратор для обработки POST-запросов по адресу "/book"
@app.route('/book', methods=['POST'])
def book():
    # Получение данных из формы
    client_name = request.form['name']   # Имя клиента
    date = request.form['date']           # Выбранная дата
    time = request.form['time']           # Выбранное время
    
    # Установка соединения с базой данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # SQL-запрос для добавления новой записи
    cursor.execute('''
        INSERT INTO appointments (client_name, date, time) 
        VALUES (?, ?, ?)
    ''', (client_name, date, time))  # Передача параметров для защиты от SQL-инъекций
    # Фиксация изменений
    conn.commit()
    # Закрытие соединения
    conn.close()
    
    # Перенаправление пользователя на главную страницу
    return redirect(url_for('index'))

# Декоратор для страницы парикмахера ("/barber")
@app.route('/barber')
def barber():
    # Установка соединения с базой данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # SQL-запрос для получения всех записей
    cursor.execute('SELECT * FROM appointments')
    # Получение всех результатов запроса
    appointments = cursor.fetchall()
    # Закрытие соединения
    conn.close()
    # Отображение шаблона barber.html с передачей списка записей
    return render_template('barber.html', appointments=appointments)

# Декоратор для подтверждения записи с динамическим параметром id
@app.route('/confirm/<int:id>')
def confirm(id):
    # Установка соединения с базой данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # SQL-запрос для обновления статуса записи по ID
    cursor.execute('UPDATE appointments SET status="confirmed" WHERE id=?', (id,))
    # Фиксация изменений
    conn.commit()
    # Закрытие соединения
    conn.close()
    # Перенаправление на страницу парикмахера
    return redirect(url_for('barber'))

# Проверка, что скрипт запущен напрямую, а не импортирован
if __name__ == '__main__':
    # Запуск Flask приложения в режиме отладки
    app.run(debug=True)
