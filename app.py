from flask import Flask, render_template, request, redirect, url_for,session,flash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Создаем таблицу студентов, если она не существует
conn = sqlite3.connect('students.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              email TEXT NOT NULL,
              course INTEGER,
              groups TEXT NOT NULL,
              birthdate DATE
              )''')
conn.commit()
conn.close()

def check_login(username, password):
    # здесь можно проверить логин и пароль
    # и вернуть True, если они верны, и False в противном случае
    if username == 'admin' and password == 'secret':
        return True
    else:
        return False

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Вы вышли из системы')
    return redirect(url_for('index'))


# Главная страница со списком студентов
@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Страница добавления нового студента
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        groups = request.form['groups']
        birthdate = request.form['birthdate']
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, email,course,groups,birthdate) VALUES (?, ?,?,?,?)", (name, email,course,groups,birthdate))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        return render_template('add.html')

# Страница редактирования студента
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        groups = request.form['groups']
        birthdate = request.form['birthdate']
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("UPDATE students SET name=?, email=? ,course=? ,groups=?, birthdate=? WHERE id=?", (name, email,course,groups,birthdate, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE id=?", (id,))
        student = c.fetchone()
        conn.close()
        return render_template('edit.html', student=student)

# Страница удаления студента
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Проверяем логин и пароль
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Вы успешно вошли в систему')
            return redirect(url_for('index'))
        else:
            flash('Неправильный логин или пароль')
    return render_template('login.html')



if __name__ == '__main__':
    app.run(port=5000)
