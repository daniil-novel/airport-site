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

def execute_query(query):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def execute_query_with_result(query, fetch=True):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
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
    return render_template('form_reg_users.html')  # Можете заменить на 'form_reg_admins.html' если нужно


if __name__ == '__main__':
    app.run(debug=True)
