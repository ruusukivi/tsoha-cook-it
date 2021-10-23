from flask import session
from db import db
import recipes

def add_photo(file, recipe_id):
    name = file.filename
    data = file.read()
    creator_id = session['user_id']
    visible = 1
    size = len(file.read())
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

def get_photo(recipe_id):
    try:
        sql = 'SELECT data FROM photos WHERE recipe_id=:recipe_id'
        result = db.session.execute(sql, {"recipe_id":recipe_id})
        return result.fetchone()[0]
    except:
        return False
