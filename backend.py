from flask import Flask, request, render_template, redirect
import os
import sqlite3

current_location = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

def create_database():
    conn = sqlite3.connect(os.path.join(current_location, 'login.db'))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(name TEXT, email VARCHAR(100), password VARCHAR(40))''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')  # Adjusted path

@app.route('/', methods=['POST'])
def checklogin():
    EM = request.form['sign-in-email']
    PW = request.form['sign-in-password']
    
    conn = sqlite3.connect(os.path.join(current_location, 'login.db'))
    cursor = conn.cursor()
    query = 'SELECT email,password FROM users WHERE email = ? AND password = ?'
    cursor.execute(query, (EM, PW))
    row = cursor.fetchone()
    conn.close()
    if row:
        return render_template('index02.html')
    else:
        return 'Sign In first!!!'

@app.route('/', methods=['GET', 'POST'])
def sign_up():   
    if request.method == 'POST':
        sName = request.form['name']
        sEM = request.form['sign-up-email']
        sPW = request.form['sign-up-password']
        
        conn = sqlite3.connect(os.path.join(current_location, 'login.db'))
        cursor = conn.cursor()
        query = 'INSERT INTO users VALUES (?, ?, ?)'
        cursor.execute(query, (sName, sEM, sPW))
        conn.commit()
        conn.close()
        return redirect('/')    
    return render_template('index.html')  
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
