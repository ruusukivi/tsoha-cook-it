from flask import session
from db import db
import datetime


def get_all():
    sql = '''SELECT R.name, R.description, U.profilename,
    R.created_at FROM recipes R, users U WHERE R.creator_id=U.id ORDER BY R.created_at'''
    result = db.session.execute(sql)
    return result.fetchall()

def add_recipe(name, description):
    creator_id = session['user_id']
    created_at = datetime.datetime.now()
    try:
        sql = '''INSERT INTO recipes (name,description,
        creator_id, created_at) VALUES (:name,:description,:creator_id,:created_at)'''
        db.session.execute(sql,
        {'name':name,'description':description,'creator_id':creator_id,'created_at':created_at})
        db.session.commit()
    except:
        return False
    return True

