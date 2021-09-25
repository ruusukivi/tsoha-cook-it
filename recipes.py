import datetime
from flask import session
from db import db

def get_all():
    sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, T.name as type,
    U.profilename, R.created_at FROM recipes R, users U, types T WHERE R.creator_id=U.id
    AND T.id=R.typeid AND R.visible=1 ORDER BY R.created_at DESC'''
    result = db.session.execute(sql)
    return result.fetchall()

def get(recipe_id):
    sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, R.creator_id,
    T.name as type, U.profilename, R.created_at FROM recipes R, users U, types T
    WHERE R.id=:recipe_id AND R.creator_id=U.id AND T.id=R.typeid AND R.visible=1'''
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    return result.fetchone()

def get_types():
    sql = 'SELECT name, id FROM types ORDER BY id'
    result = db.session.execute(sql)
    return result.fetchall()

def add_recipe(name, description, typeid, steps, ingredients):
    creator_id = session['user_id']
    created_at = datetime.datetime.now()
    visible = 1
    try:
        sql = '''INSERT INTO recipes (name,description,typeid,steps,ingredients,
        creator_id,created_at,visible) VALUES (:name,:description,:typeid,
        :steps,:ingredients,:creator_id,:created_at,:visible)'''
        db.session.execute(sql,
        {'name':name,'description':description,'typeid':typeid,
        'steps':steps,'ingredients':ingredients,'creator_id':creator_id,
        'created_at':created_at,'visible':visible})
        db.session.commit()
    except:
        return False
    return True

def get_likes(recipe):
    sql = 'SELECT COUNT(recipe) FROM likes WHERE recipe=:recipe'
    result = db.session.execute(sql, {'recipe':recipe})
    return result.fetchone()

def has_user_liked(recipe, userid):
    sql = 'SELECT id FROM likes WHERE recipe=:recipe AND userid=:userid'
    result = db.session.execute(sql, {'recipe':recipe,'userid':userid })
    return result.fetchone()

def like_recipe(recipe):
    userid = session['user_id']
    if has_user_liked(recipe, userid):
        try:
            sql = 'DELETE FROM likes WHERE recipe=:recipe AND userid=:userid'
            db.session.execute(sql,{'recipe':recipe, 'userid':userid})
            db.session.commit()
        except:
            return False
    else:
        try:
            sql = 'INSERT INTO likes (recipe, userid) VALUES (:recipe, :userid)'
            db.session.execute(sql,{'recipe':recipe, 'userid':userid})
            db.session.commit()
        except:
            return False
    return True

def delete_recipe(recipe_id):
    try:
        creator_id = session['user_id']
        sql = 'UPDATE recipes SET visible=0 WHERE id=:recipe_id AND creator_id=:creator_id'
        db.session.execute(sql,{'recipe_id':recipe_id, 'creator_id':creator_id})
        db.session.commit()
    except:
        return False
    return True
