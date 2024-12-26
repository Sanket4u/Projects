from flask import Flask, render_template, request, request, redirect, url_for
import cryptography
import pymysql
#import os

app = Flask(__name__)


# Database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin@123'
app.config['MYSQL_DB'] = 'food_order'

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    

#landing on index page
@app.route('/')
def index():
    return render_template('index.html', message = 'Submit')


#submit the form
@app.route("/submit", methods = ['POST'])
def submit():
    name = request.form['name']
    items = request.form['items']
    price = request.form['price']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tbl_foodorder (name,items,price) VALUES (%s,%s,%s)', (name,items,price))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001,debug=True)
