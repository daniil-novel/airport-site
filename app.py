# app.py

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Замените 'ваш_username' и 'ваш_password' на свои реальные учетные данные
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '20161620Aa',
    'database': 'airport',
    'raise_on_warnings': True
}

def execute_query(query, values=None):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()  # Добавляем команду commit
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def execute_query_with_result(query, fetch=True, values=None):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def register_user(username, password, hometown):
    # Вставка записи пользователя
    insert_user_query = f"INSERT INTO Users (username, password, hometown) VALUES ('{username}', '{password}', '{hometown}');"
    execute_query_with_result(insert_user_query, fetch=False)

def register_admin(admin_id, password):
    # Вставка записи админа
    insert_admin_query = f"INSERT INTO Admins (id, password) VALUES ('{admin_id}', '{password}');"
    execute_query_with_result(insert_admin_query, fetch=False)

def validate_user_credentials(username, password):
    # Проверка существования пользователя с указанным именем и паролем
    query = f"SELECT * FROM Users WHERE username = '{username}' AND password = '{password}';"
    result = execute_query_with_result(query)
    return bool(result)

def validate_admin_credentials(admin_id, password):
    # Проверка существования админа с указанным ID и паролем
    query = f"SELECT * FROM Admins WHERE id = '{admin_id}' AND password = '{password}';"
    result = execute_query_with_result(query)
    return bool(result)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form-reg', methods=['GET', 'POST'])
def registration_form():
    if request.method == 'POST':
        # Проверка наличия всех необходимых полей в запросе
        if 'userType' not in request.form:
            return "Invalid request. Missing required fields."

        user_type = request.form['userType']

        # В зависимости от типа пользователя перенаправляем на соответствующую форму
        if user_type == 'user':
            return render_template('form_reg_users.html')
        elif user_type == 'admin':
            return render_template('form_reg_admins.html')

    # Если это GET запрос или другие случаи, показываем форму выбора типа пользователя
    return render_template('form_reg.html', user_type='user')  # или 'admin'

@app.route('/register-user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Регистрация пользователя
        username = request.form.get('username')
        password = request.form.get('password')
        hometown = request.form.get('hometown')

        # Ваша логика регистрации пользователя
        insert_user_query = "INSERT INTO Users (username, password, hometown) VALUES (%s, %s, %s);"
        values = (username, password, hometown)
        try:
            execute_query_with_result(insert_user_query, fetch=False, values=values)
            print("User registered successfully!")
        except Exception as e:
            print(f"Error registering user: {e}")

        # После регистрации перенаправляем на главную страницу
        return redirect(url_for('index'))

    # Если это GET запрос или другие случаи, отобразим форму регистрации пользователя
    return render_template('form_reg.html')

@app.route('/register-admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        # Регистрация администратора
        admin_id = request.form.get('adminId')
        admin_password = request.form.get('adminPassword')

        # Ваша логика регистрации администратора
        insert_admin_query = "INSERT INTO Admins (id, password) VALUES (%s, %s);"
        values = (admin_id, admin_password)
        try:
            execute_query_with_result(insert_admin_query, fetch=False, values=values)
            print("Admin registered successfully!")
        except Exception as e:
            print(f"Error registering admin: {e}")

        # После регистрации администратора перенаправляем на главную страницу
        return redirect(url_for('index'))

    # Если это GET запрос или другие случаи, отобразим форму регистрации администратора
    return render_template('form_reg.html')


if __name__ == '__main__':
    app.run(debug=True)
