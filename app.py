import requests
from flask import Flask,render_template,request,redirect
import psycopg2

app= Flask(__name__)

conn = psycopg2.connect(database="service_db",
user="postgres", password="1111", host="localhost", port="5432")

cursor = conn.cursor()


@app.route('/', methods=['GET'])
def index():
    return redirect('/login/')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if name is None or login is None or password is None or (len(name) == 0 or len(login) == 0 or len(password)==0):
            return render_template('registration.html', error='login or password or name is empty')

        cursor.execute(f"SELECT * FROM service.users WHERE login='{str(login)}'")
        records = list(cursor.fetchall())
        if len(records)>0:
            return render_template('registration.html', error='user already exist')

        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',(str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html',error='')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password =request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect('/registration/')
    return render_template('login.html')






if __name__ == '__main__':
    app.run()

