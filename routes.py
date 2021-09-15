from flask import render_template, redirect, request
from app import app
import users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            return redirect('/')
    return render_template('error.html')

@app.route('/logout')
def logout():
    users.logout()

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        profilename = request.form['profilename']
        if password != password2:
            return render_template('error.html')
        if users.signup(username, password, profilename):
            return redirect('/')
    return render_template('error.html')
