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
    return render_template('login.html', message='Please check username and password')

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        profilename = request.form['profilename']
        if len(password) < 9:
            return render_template('signup.html', message='Ooops! Password is too short')
        if password != password2:
            return render_template('signup.html', message='Oops! Passwords do not match')
        if users.signup(username, password, profilename):
            return render_template('login.html', message='Sign up done! Please log in')
    return render_template('error.html', message='Sign up failed.')
