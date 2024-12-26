from flask import Flask, render_template, request, jsonify, redirect, url_for
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import json

app = Flask(__name__)

# Database connection details (Consider using SQLAlchemy instead of pymysql directly)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin@123' #  **Important:** Do not hardcode passwords in production. Use environment variables.
app.config['MYSQL_DB'] = 'food_order'

def get_db_connection():
    try:
        return pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
    except pymysql.Error as e:
        return None #or handle the error appropriately, perhaps logging it

@app.route('/admin', methods=['GET'])
def admin():
    conn = get_db_connection()
    if conn is None:
        return "Database connection error", 500 #Improved error handling

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT name, items, price FROM tbl_foodorder')
        orders = cursor.fetchall()  # Fetch all results
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('admin.html', orders=orders) #Render the template
    except pymysql.Error as e:
        return f"Database error: {e}", 500 #Improved error handling
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500 #Improved error handling



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)