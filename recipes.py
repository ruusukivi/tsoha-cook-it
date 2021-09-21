import datetime
from flask import session
from db import db

def get_all():
    sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, T.name as type,
    U.profilename, R.created_at FROM recipes R, users U, types T WHERE R.creator_id=U.id
    AND T.id=R.typeid ORDER BY R.created_at DESC'''
    result = db.session.execute(sql)
    return result.fetchall()

def get(id):
    sql = '''SELECT R.name, R.description, R.ingredients, R.steps, T.name as type, U.profilename,
    R.created_at FROM recipes R, users U, types T WHERE R.id=:id AND 
    R.creator_id=U.id AND T.id=R.typeid'''
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_types():
    sql = 'SELECT name, id FROM types ORDER BY id'
    result = db.session.execute(sql)
    return result.fetchall()

def add_recipe(name, description, typeid, steps, ingredients):
    creator_id = session['user_id']
    created_at = datetime.datetime.now()
    try:
        sql = '''INSERT INTO recipes (name,description,typeid,steps,ingredients,
        creator_id,created_at) VALUES (:name,:description,:typeid,
        :steps,:ingredients,:creator_id,:created_at)'''
        db.session.execute(sql,
        {'name':name,'description':description,'typeid':typeid,
        'steps':steps,'ingredients':ingredients,'creator_id':creator_id,
        'created_at':created_at})
        print('päästään session jälkeen')
        db.session.commit()
    except:
        return False
    return True

