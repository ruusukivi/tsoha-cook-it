import os
from flask import session, request
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = 'SELECT id, password FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['username'] = username
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False

def logout():
    del session['user_id'], session['username']

def signup(username, password, profilename):
    hash_value = generate_password_hash(password)
    try:
        sql = '''INSERT INTO users (username,password,
        profilename) VALUES (:username,:password,:profilename)'''
        db.session.execute(sql,
        {'username':username,'password':hash_value,'profilename':profilename})
        db.session.commit()
    except:
        return False
    return True

def user_id():
    return session.get('user_id',0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
