from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Создание базы данных
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY,
            client_name TEXT,
            date TEXT,
            time TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Главная страница
@app.route('/')
def index():
    return render_template('client.html')

# Клиент: записаться
@app.route('/book', methods=['POST'])
def book():
    client_name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (client_name, date, time) 
        VALUES (?, ?, ?)
    ''', (client_name, date, time))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Парикмахер: просмотр записей
@app.route('/barber')
def barber():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments')
    appointments = cursor.fetchall()
    conn.close()
    return render_template('barber.html', appointments=appointments)

# Парикмахер: подтвердить запись
@app.route('/confirm/<int:id>')
def confirm(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE appointments SET status="confirmed" WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('barber'))

if __name__ == '__main__':
    app.run(debug=True)