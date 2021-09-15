from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = 'SELECT id, password FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            return True
        return False

def logout():
    del session['user_id']

def signup(username, password, profilename):
    print ('Sign up started')
    hash_value = generate_password_hash(password)
    try:
        sql = 'INSERT INTO users (username,password,profilename) VALUES (:username,:password,:profilename)'
        print ('Insert done')
        db.session.execute(sql, {'username':username,'password':hash_value,'profilename':profilename})
        print ('Execute done')
        db.session.commit()
        print ('Session done')
    except:
        print ('Error in signup')
        return False
    return login(username, password)

def user_id():
    return session.get('user_id',0)

