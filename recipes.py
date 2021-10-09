from flask import session
from db import db

# Getting, adding and deleting recipes

def get_all():
    sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps,
    T.name AS type,U.profilename, R.created_at,
    R.like_count, R.comment_count
    FROM recipes R LEFT JOIN users U ON R.creator_id=U.id 
    LEFT JOIN types T ON T.id=R.typeid
    WHERE R.visible=1 GROUP BY R.id, U.id, T.id ORDER BY R.created_at DESC'''
    result = db.session.execute(sql)
    return result.fetchall()

def get_popular():
    sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, T.name AS type,
    U.profilename, R.created_at,  R.like_count, R.comment_count
    FROM recipes R, users U, types T
    WHERE R.creator_id=U.id AND T.id=R.typeid AND R.visible=1
    GROUP BY R.id, U.profilename, T.name
    ORDER BY R.like_count DESC'''
    result = db.session.execute(sql)
    return result.fetchall()

def get(recipe_id):
    sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, R.creator_id,
    T.name as type, U.profilename, R.created_at, R.like_count, R.comment_count
    FROM recipes R, users U, types T
    WHERE R.id=:recipe_id AND R.creator_id=U.id AND T.id=R.typeid AND R.visible=1'''
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    return result.fetchone()

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

def delete_recipe(recipe_id):
    try:
        creator_id = session['user_id']
        sql = 'UPDATE recipes SET visible=0 WHERE id=:recipe_id AND creator_id=:creator_id'
        db.session.execute(sql,{'recipe_id':recipe_id, 'creator_id':creator_id})
        db.session.commit()
    except:
        return False
    return True

# Getting recipes for profile page

def get_recipes(profilename):
    try:
        sql = '''SELECT R.id, R.name, R.description, T.name AS type, U.profilename,
        R.created_at, R.like_count, R.comment_count
        FROM recipes R LEFT JOIN users U ON R.creator_id=U.id 
        LEFT JOIN types T ON T.id=R.typeid
        WHERE R.visible=1 AND U.profilename=:profilename
        GROUP BY R.id, U.id, T.id ORDER BY R.created_at DESC'''
        result = db.session.execute(sql,{'profilename':profilename})
        return result.fetchall()
    except:
        return False

def get_profile_likes(profilename):
    try:
        sql = '''SELECT R.id, R.name, R.description, T.name AS type,U.profilename,
        R.created_at, R.like_count, R.comment_count
        FROM recipes R, users U, types T
        WHERE R.creator_id=U.id AND T.id=R.typeid AND R.visible=1
        GROUP BY R.id, U.profilename, T.name ORDER BY like_count DESC;'''
        result = db.session.execute(sql,{'profilename':profilename})
        return result.fetchall()
    except:
        return False

def get_profile_commented(profilename):
    try:
        sql = '''SELECT R.id, R.name, R.description, T.name AS type,U.profilename,
        R.created_at, R.like_count, R.comment_count
        FROM recipes R, users U, types T
        WHERE R.creator_id=U.id AND T.id=R.typeid AND R.visible=1
        GROUP BY R.id, U.profilename, T.name ORDER BY like_count DESC;'''
        result = db.session.execute(sql,{'profilename':profilename})
        return result.fetchall()
    except:
        return False


# Getting types

def get_types():
    sql = 'SELECT name, id FROM types ORDER BY id'
    result = db.session.execute(sql)
    return result.fetchall()

# Getting, counting, adding and deleting comments

def get_comments_count(recipe_id):
    sql = 'SELECT COUNT(recipe_id) FROM comments WHERE recipe_id=:recipe_id'
    result = db.session.execute(sql, {'recipe_id':recipe_id})
    return result.fetchone()

def get_comments(recipe_id):
    sql = '''SELECT C.id, C.title, C.comment, U.profilename, C.created_at
    FROM comments C, users U
    WHERE C.recipe_id=:recipe_id AND C.author_id=U.id AND C.visible=1
    GROUP BY C.id, U.id ORDER BY C.created_at DESC'''
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    return result.fetchall()

def has_user_commented(recipe_id, author_id):
    sql = 'SELECT id FROM comments WHERE recipe_id=:recipe_id AND author_id=:author_id'
    result = db.session.execute(sql, {'recipe_id':recipe_id,'author_id':author_id })
    return result.fetchone()

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

# Getting, counting, adding and deleting likes

def get_like_count(recipe_id):
    sql = 'SELECT COUNT(recipe_id) FROM likes WHERE recipe_id=:recipe_id'
    result = db.session.execute(sql, {'recipe_id':recipe_id})
    return result.fetchone()

def has_user_liked(recipe_id, liker_id):
    sql = 'SELECT id FROM likes WHERE recipe_id=:recipe_id AND liker_id=:liker_id'
    result = db.session.execute(sql, {'recipe_id':recipe_id,'liker_id':liker_id })
    return result.fetchone()

def like_recipe(recipe_id):
    liker_id = session['user_id']
    if has_user_liked(recipe_id, liker_id):
        try:
            sql = 'DELETE FROM likes WHERE recipe_id=:recipe_id AND liker_id=:liker_id'
            db.session.execute(sql,{'recipe_id':recipe_id, 'liker_id':liker_id})
            db.session.commit()
            update_recipe_like_count(recipe_id)
        except:
            return False
    else:
        try:
            sql = 'INSERT INTO likes (recipe_id, liker_id) VALUES (:recipe_id, :liker_id)'
            db.session.execute(sql,{'recipe_id':recipe_id, 'liker_id':liker_id})
            db.session.commit()
        except:
            return False
    return True

def update_recipe_like_count(recipe_id):
    count = get_like_count(recipe_id) + 1
    sql = 'UPDATE recipe SET like_count=:count WHERE id=:recipe_id'
    result = db.session.execute(sql, {'recipe_id':recipe_id , 'like_count':count})
    return result.fetchone()
