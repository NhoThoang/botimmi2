from threading import Thread
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

class mysql_data:
    def __init__(self, host=None, user=None, password=None, database=None, table=None):
        self.host = host
        self.user_host = user
        self.password_host = password
        self.database = database
        self.table = table
       
    def create_database(self):
        connect = mysql.connector.connect(host=self.host, user=self.user_host, password=self.password_host)
        cursor = connect.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')
        cursor.execute(f'USE {self.database}')
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.table}(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            passport VARCHAR(255),
            phone VARCHAR(255),
            approval BOOLEAN NOT NULL
        )""")
        connect.commit()
        cursor.close()


host = "localhost"
user = "root"
password = "123456"
database_name = "user_data"
table_name = "customers"

mysql_instance = mysql_data(host, user, password, database_name, table_name)
Thread(target=mysql_instance.create_database).start()

app = Flask(__name__)
app.secret_key = 'nhothoang'
app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = database_name
mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and "passport" in request.form:
        username = request.form['username']
        password = request.form['password']
        passport = request.form['passport']
        # approval = 1
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM {table_name} WHERE username = %s AND password = %s AND passport = %s AND approval = %s', (username, password,passport, 1))
        customer = cursor.fetchone()
        if customer:
            session['loggedin'] = True
            session['id'] = customer['id']
            session['username'] = customer['username']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username, password, or passport. Please try again.'

    return render_template('login.html', msg=msg)
            # cursor.execute(f'SELECT * FROM {table_name} WHERE username = %s', (username,))
            # user_exists = cursor.fetchone()
            
            # cursor.execute(f'SELECT * FROM {table_name} WHERE password = %s', (password,))
            # password_exists = cursor.fetchone()

            # cursor.execute(f'SELECT * FROM {table_name} WHERE passport = %s', (passport,))
            # passport_exists = cursor.fetchone()

            # if user_exists:
            #     msg = 'Incorrect password or passport.'
            # elif password_exists:
            #     msg = 'Incorrect username or passport.'
            # elif passport_exists:
            #     msg = 'Incorrect username or password.'
            # else:
            #     msg = 'Incorrect username, password, and passport.'
            
    # return render_template('login.html', msg=msg)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password'  in request.form and 'passport' in request.form and "phone" in request.form:
        username = request.form['username']
        password = request.form['password']
        # email = request.form['email']
        passport = request.form["passport"]
        phone  = request.form["phone"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(f'SELECT * FROM {table_name} WHERE username = %s OR passport = %s', (username, passport,))
        existing_user = cursor.fetchone()
        if existing_user:
            if existing_user['username'] == username:
                msg = 'Username already exists!'
            else:
                msg = 'Passport already exists!'
        # cursor.execute(f'SELECT * FROM {table_name} WHERE username = %s AND passport = %s', (username, passport, ))
        # existing_user = cursor.fetchone()
        # if existing_user:
        #     msg = 'Account already exists!'

        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not passport or not phone:
        # elif not username or not password or not email or not passport or not phone:
            msg = 'Please fill out the form!'
        # elif not username or not password or not email:g
        #     msg = 'Please fill out the form!'
        else:
            cursor.execute(f'INSERT INTO {table_name} (username, password, passport, phone, approval) VALUES (%s, %s, %s, %s, %s)', (username, password, passport, phone, 0,))

            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/approval', methods=['GET', 'POST'])
def approval():
    msg = ''
    if request.method == 'POST' and "passport" in request.form:
        passport = request.form['passport']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM {table_name} WHERE passport = %s", (passport,))
            customer = cursor.fetchone()

            if customer:
                msg = 'Logged in successfully!'
                cursor.execute(f"UPDATE {table_name} SET approval = 1 WHERE passport = %s", (passport,))
                mysql.connection.commit()  # Commit thay đổi vào database
                return render_template('index.html', msg=msg)
            else:
                msg = 'Incorrect passport. Please try again.'
        except mysql.connector.Error as err:
            msg = f"Error: {err}"
        finally:
            cursor.close()
    return render_template('approval.html', msg=msg)


@app.route('/disapproval', methods=['GET', 'POST'])
def disapproval():
    msg = ''
    if request.method == 'POST' and "passport" in request.form:
        passport = request.form['passport']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM {table_name} WHERE passport = %s", (passport,))
            customer = cursor.fetchone()

            if customer:
                msg = 'Logged in successfully!'
                cursor.execute(f"UPDATE {table_name} SET approval = 0 WHERE passport = %s", (passport,))
                mysql.connection.commit()  # Commit thay đổi vào database
                return render_template('index.html', msg=msg)
            else:
                msg = 'Incorrect passport. Please try again.'
        except mysql.connector.Error as err:
            msg = f"Error: {err}"
        finally:
            cursor.close()
    return render_template('disapproval.html', msg=msg)



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True, port=5000)