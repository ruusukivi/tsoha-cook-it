from flask import session
from db import db

def get_all():
    sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps,
    T.name AS type,U.profilename, R.created_at,
    count(L.recipe) AS popularity, count(C.recipe_id) AS comments
    FROM recipes R LEFT JOIN users U ON R.creator_id=U.id 
    LEFT JOIN types T ON T.id=R.typeid
    LEFT JOIN likes L ON L.recipe = R.id
    LEFT JOIN comments C ON C.recipe_id = R.id
    WHERE R.visible=1 GROUP BY R.id, U.id, T.id, C.id ORDER BY R.created_at DESC'''
    result = db.session.execute(sql)
    return result.fetchall()

def get_popular():
    sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, T.name AS type,
    U.profilename, R.created_at, count(L.recipe) AS popularity 
    FROM recipes R, users U, types T, likes L
    WHERE R.creator_id=U.id AND T.id=R.typeid AND R.visible=1 AND L.recipe = R.id
    GROUP BY R.id, U.profilename, T.name
    ORDER BY popularity DESC'''
    result = db.session.execute(sql)
    return result.fetchall()

def get(recipe_id):
    sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, R.creator_id,
    T.name as type, U.profilename, R.created_at FROM recipes R, users U, types T
    WHERE R.id=:recipe_id AND R.creator_id=U.id AND T.id=R.typeid AND R.visible=1'''
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    return result.fetchone()

def get_recipes(profilename):
    try:
        sql = '''SELECT R.id, R.name, R.description, T.name AS type, U.profilename,
        R.created_at, count(L.recipe) AS popularity
        FROM recipes R LEFT JOIN users U ON R.creator_id=U.id 
        LEFT JOIN types T ON T.id=R.typeid
        LEFT JOIN likes L ON L.recipe = R.id
        WHERE R.visible=1 AND U.profilename=:profilename
        GROUP BY R.id, U.id, T.id ORDER BY R.created_at DESC'''
        result = db.session.execute(sql,{'profilename':profilename})
        return result.fetchall()
    except:
        return False

def get_types():
    sql = 'SELECT name, id FROM types ORDER BY id'
    result = db.session.execute(sql)
    return result.fetchall()

def add_recipe(name, description, typeid, steps, ingredients):
    creator_id = session['user_id']
    visible = 1
    try:
        sql = '''INSERT INTO recipes (name,description,typeid,steps,ingredients,
        creator_id,created_at,visible) VALUES (:name,:description,:typeid,
        :steps,:ingredients,:creator_id,now(),:visible)'''
        db.session.execute(sql,
        {'name':name,'description':description,'typeid':typeid,
        'steps':steps,'ingredients':ingredients,'creator_id':creator_id,'visible':visible})
        db.session.commit()
    except:
        return False
    return True

def add_comment(title, comment, recipe_id):
    author_id = session['user_id']
    visible = 1
    try:
        sql = '''INSERT INTO comments(title,comment,author_id,recipe_id,created_at,visible) VALUES
        (:title,:comment,:author_id,:recipe_id,now(),:visible)'''
        db.session.execute(sql,{'title':title,'comment':comment,'author_id':author_id,
        'recipe_id':recipe_id,'visible':visible})
        db.session.commit()
    except:
        return False
    return True

def get_comments(recipe_id):
    sql = '''SELECT C.id, C.title, C.comment, U.profilename, C.created_at
    FROM comments C, users U
    WHERE C.recipe_id=:recipe_id AND C.author_id=U.id AND C.visible=1
    GROUP BY C.id, U.id ORDER BY C.created_at DESC'''
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    return result.fetchall()

def get_likes(recipe):
    sql = 'SELECT COUNT(recipe) FROM likes WHERE recipe=:recipe'
    result = db.session.execute(sql, {'recipe':recipe})
    return result.fetchone()

def get_comments_count(recipe_id):
    sql = 'SELECT COUNT(recipe_id) FROM comments WHERE recipe_id=:recipe_id'
    result = db.session.execute(sql, {'recipe_id':recipe_id})
    return result.fetchone()

def get_profile_likes(profilename):
    try:
        sql = '''SELECT R.id, R.name, R.description, T.name AS type,U.profilename,
        R.created_at, count(L.recipe) AS popularity 
        FROM recipes R, users U, types T, likes L
        WHERE R.creator_id=U.id AND T.id=R.typeid AND R.visible=1 AND L.userid=U.id AND L.recipe=R.id 
        GROUP BY R.id, U.profilename, T.name ORDER BY popularity DESC;'''
        result = db.session.execute(sql,{'profilename':profilename})
        return result.fetchall()
    except:
        return False

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
