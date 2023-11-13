# app.py

from flask import Flask, render_template, jsonify
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/airport_info/<user_type>')
def get_airport_info(user_type):
    if user_type == 'admin':
        query = "SELECT * FROM Flight;"
    else:
         query = "SELECT * FROM Flight;"

    result = execute_query(query)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
