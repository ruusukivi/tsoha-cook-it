import os
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = 'SELECT id, password, profilename, admin FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['username'] = username
        session['profilename'] = user.profilename
        session['admin'] = user.admin
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False

def logout():
    if user_id():
        del session['user_id']
        del session['username']
        del session['profilename']
        del session['admin']
        del session['csrf_token']

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

def update_admin_rights(profilename):
    try:
        sql = 'UPDATE users SET admin=True WHERE profilename=:profilename'
        db.session.execute(sql,{'profilename':profilename})
        db.session.commit()
    except:
        return False
    return True

def is_username_taken(username):
    sql = 'SELECT username FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username':username})
    return result.fetchone()

def is_profilename_taken(profilename):
    sql = 'SELECT profilename FROM users WHERE profilename=:profilename'
    result = db.session.execute(sql, {'profilename':profilename})
    return result.fetchone()

def user_id():
    return session.get('user_id',0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
