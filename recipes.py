from flask import session
from db import db

# Recipes for front page

def get_all():
    try:
        sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps,
        T.name AS type,U.profilename, R.created_at, R.like_count, R.comment_count
        FROM recipes R, users U, types T
        WHERE R.creator_id=U.id AND T.id=R.typeid AND R.visible=1 
        GROUP BY R.id, U.id, T.id 
        ORDER BY R.created_at DESC'''
        result = db.session.execute(sql)
        return result.fetchall()
    except:
        return False
    return True

def get_popular():
    try:
        sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, T.name AS type,
        U.profilename, R.created_at,  R.like_count, R.comment_count
        FROM recipes R, users U, types T
        WHERE R.creator_id=U.id AND T.id=R.typeid AND R.visible=1 AND R.like_count>0
        GROUP BY R.id, U.id, T.id
        ORDER BY R.like_count DESC'''
        result = db.session.execute(sql)
        return result.fetchall()
    except:
        return False
    return True

def get_commented():
    try:
        sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, T.name AS type,
        U.profilename, R.created_at, R.like_count, R.comment_count
        FROM recipes R, users U, types T
        WHERE R.creator_id=U.id AND T.id=R.typeid AND R.visible=1 AND R.comment_count>0
        GROUP BY R.id, U.profilename, T.name
        ORDER BY R.comment_count DESC'''
        result = db.session.execute(sql)
        return result.fetchall()
    except:
        return False

# Getting, adding and deleting a recipe

def get(recipe_id):
    try:
        sql = '''SELECT R.id, R.name, R.description, R.ingredients, R.steps, R.creator_id,
        T.name as type, U.profilename, R.created_at, R.like_count, R.comment_count
        FROM recipes R, users U, types T
        WHERE R.id=:recipe_id AND R.creator_id=U.id AND T.id=R.typeid AND R.visible=1'''
        result = db.session.execute(sql, {"recipe_id":recipe_id})
        return result.fetchone()
    except:
        return False

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
        if session['admin']:
            sql = 'UPDATE recipes SET visible=0 WHERE id=:recipe_id'
            db.session.execute(sql,{'recipe_id':recipe_id})
        else:
            creator_id = session['user_id']
            sql = 'UPDATE recipes SET visible=0 WHERE id=:recipe_id AND creator_id=:creator_id'
            db.session.execute(sql,{'recipe_id':recipe_id, 'creator_id':creator_id})
        db.session.commit()
    except:
        return False
    return True

# Getting recipe types

def get_types():
    try:
        sql = 'SELECT name, id FROM types ORDER BY id'
        result = db.session.execute(sql)
        return result.fetchall()
    except:
        return False

# Getting recipes for profile page

def get_profile_id(profilename):
    try:
        sql = 'SELECT id FROM users WHERE profilename=:profilename'
        result = db.session.execute(sql,{'profilename':profilename})
        return result.fetchone()
    except:
        return False

def get_recipes(profilename):
    try:
        sql = '''SELECT R.id, R.name, R.description, T.name AS type, U.profilename,
        R.created_at, R.like_count, R.comment_count
        FROM recipes R LEFT JOIN users U ON R.creator_id=U.id 
        LEFT JOIN types T ON T.id=R.typeid
        WHERE R.visible=1 AND U.profilename=:profilename
        GROUP BY R.id, U.id, T.id 
        ORDER BY R.created_at DESC'''
        result = db.session.execute(sql,{'profilename':profilename})
        return result.fetchall()
    except:
        return False

def get_profile_likes(profilename):
    try:
        liker = get_profile_id(profilename)[0]
        sql = '''SELECT L.liker_id, R.id, R.name, R.description, T.name AS type,
        U.profilename, R.created_at, R.like_count, R.comment_count 
        FROM likes L JOIN recipes R ON L.recipe_id=R.id 
        LEFT JOIN users U ON U.id=L.liker_id 
        LEFT JOIN types T ON T.id=R.typeid 
        WHERE R.visible=1 AND L.liker_id=:liker 
        GROUP BY L.liker_id, R.id, U.id, T.id
        ORDER BY R.created_at DESC'''
        result = db.session.execute(sql, {'liker':liker})
        return result.fetchall()
    except:
        return False

def get_profile_commented(profilename):
    try:
        author = get_profile_id(profilename)[0]
        sql = '''SELECT C.author_id, R.id, R.name, R.description, T.name AS type,
        U.profilename, R.created_at, R.like_count, R.comment_count 
        FROM comments C JOIN recipes R ON C.recipe_id=R.id 
        LEFT JOIN users U ON U.id=C.author_id 
        LEFT JOIN types T ON T.id=R.typeid 
        WHERE R.visible=1 AND C.visible=1 AND C.author_id=:author 
        GROUP BY C.author_id, R.id, U.id, T.id
        ORDER BY R.created_at DESC'''
        result = db.session.execute(sql, {'author':author})
        return result.fetchall()
    except:
        return False

# Comments: comment count for lists, comments for recipe page,
# adding and deleting a comment

def get_comments_count(recipe_id):
    try:
        sql = 'SELECT COUNT(recipe_id) FROM comments WHERE recipe_id=:recipe_id AND visible=1'
        result = db.session.execute(sql, {'recipe_id':recipe_id})
        return result.fetchone()
    except:
        return False

def get_comments(recipe_id):
    try:
        sql = '''SELECT C.id, C.title, C.comment, U.profilename,
        C.created_at, C.author_id, C.recipe_id
        FROM comments C, users U
        WHERE C.recipe_id=:recipe_id AND C.author_id=U.id AND C.visible=1
        GROUP BY C.id, U.id ORDER BY C.created_at DESC'''
        result = db.session.execute(sql, {"recipe_id":recipe_id})
        return result.fetchall()
    except:
        return False

def has_user_commented(recipe_id, author_id):
    try:
        sql = 'SELECT id FROM comments WHERE recipe_id=:recipe_id AND author_id=:author_id'
        result = db.session.execute(sql, {'recipe_id':recipe_id,'author_id':author_id })
        return result.fetchone()
    except:
        return False

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
    update_recipe_comment_count(recipe_id)
    return True

def delete_comment(comment_id, recipe_id):
    try:
        if session['admin']:
            sql = 'UPDATE comments SET visible=0 WHERE id=:comment_id'
            db.session.execute(sql,{'comment_id':comment_id})
        else:
            author_id = session['user_id']
            sql = 'UPDATE comments SET visible=0 WHERE id=:comment_id AND author_id=:author_id'
            db.session.execute(sql,{'comment_id':comment_id, 'author_id':author_id})
        db.session.commit()
    except:
        return False
    update_recipe_comment_count(recipe_id)
    return True

def update_recipe_comment_count(recipe_id):
    try:
        comment_count = get_comments_count(recipe_id)[0]
        sql = 'UPDATE recipes SET comment_count=:comment_count WHERE id=:recipe_id'
        db.session.execute(sql, {'recipe_id':recipe_id, 'comment_count':comment_count})
        db.session.commit()
    except:
        return False
    return True

# Likes: like count for lists, like for recipe page

def get_like_count(recipe_id):
    try:
        sql = 'SELECT COUNT(recipe_id) FROM likes WHERE recipe_id=:recipe_id'
        result = db.session.execute(sql, {'recipe_id':recipe_id})
        return result.fetchone()
    except:
        return False

def has_user_liked(recipe_id, liker_id):
    try:
        sql = 'SELECT id FROM likes WHERE recipe_id=:recipe_id AND liker_id=:liker_id'
        result = db.session.execute(sql, {'recipe_id':recipe_id,'liker_id':liker_id })
        return result.fetchone()
    except:
        return False

def like_recipe(recipe_id):
    liker_id = session['user_id']
    if has_user_liked(recipe_id, liker_id):
        try:
            sql = 'DELETE FROM likes WHERE recipe_id=:recipe_id AND liker_id=:liker_id'
            db.session.execute(sql,{'recipe_id':recipe_id, 'liker_id':liker_id})
            db.session.commit()
        except:
            return False
    else:
        try:
            sql = 'INSERT INTO likes (recipe_id, liker_id) VALUES (:recipe_id, :liker_id)'
            db.session.execute(sql,{'recipe_id':recipe_id, 'liker_id':liker_id})
            db.session.commit()
        except:
            return False
    update_recipe_like_count(recipe_id)
    return True

def update_recipe_like_count(recipe_id):
    try:
        like_count = get_like_count(recipe_id)[0]
        sql = 'UPDATE recipes SET like_count=:like_count WHERE id=:recipe_id'
        db.session.execute(sql, {'recipe_id':recipe_id , 'like_count':like_count})
        db.session.commit()
    except:
        return False
    return True
