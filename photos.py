from flask import session, make_response
from db import db

def add_photo(name, data, size, recipe_id):
    creator_id = session['user_id']
    visible = 1
    try:
        sql = '''INSERT INTO photos (name,data,size,recipe_id,creator_id,created_at,visible)
        VALUES (:name,:data,:size,:recipe_id,:creator_id,now(),:visible)'''
        db.session.execute(sql,
        {'name':name,'data':data,'size':size,'recipe_id':recipe_id,'creator_id':creator_id,
        'visible':visible})
        db.session.commit()
    except:
        return False
    return True

def get_photo(photo_id):
    try:
        sql = 'SELECT data FROM photos WHERE id=:photo_id AND visible=1'
        result = db.session.execute(sql, {'photo_id':photo_id})
        data = result.fetchone()[0]
        response = make_response(bytes(data))
        response.headers.set('Content-Type', 'image/jpeg')
        return response
    except:
        return False

def get_photo_id(recipe_id):
    try:
        sql = 'SELECT id FROM photos WHERE recipe_id=:recipe_id AND visible=1'
        result = db.session.execute(sql, {'recipe_id':recipe_id})
        return result.fetchone()[0]
    except:
        return False

def delete_photo(recipe_id):
    sql = 'UPDATE photos SET visible=0 WHERE recipe_id=:recipe_id AND visible=1'
    db.session.execute(sql, {'recipe_id':recipe_id})
    db.session.commit()
    return True
