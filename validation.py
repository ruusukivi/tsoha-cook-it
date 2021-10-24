from flask import flash
import users
import recipes

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def validate_signup(password, password2, username, profilename):
    if '@' not in username or users.is_username_taken(username):
        flash('Oops! Username should be an unique email address', 'error')
        return False
    if len(username) > 50 :
        flash('Oops! Username is too long', 'error')
        return False
    if users.is_profilename_taken(profilename):
        flash('Oops! Profilename is already taken.', 'error')
        return False
    if (len(password) < 9) or (len(password) > 50):
        flash('Oops! Password should have > 8 and < 50 characters', 'error')
        return False
    if password != password2:
        flash('Oops! Passwords do not match', 'error')
        return False
    return True

def validate_recipe(name, description, typeid, steps, ingredients):
    if len(name) > 150:
        flash('Oops! Name is too long', 'error')
        return False
    if typeid=="Choose":
        flash('Oops! Please choose type of the recipe', 'error')
        return False
    if len(description) > 250:
        flash('Oops! Description is too long.', 'error')
        return False
    if len(steps) > 1500:
        flash('Oops! Too much text in Steps.', 'error')
        return False
    if len(ingredients) > 1500:
        flash('Oops! Too much text in Ingredients.', 'error')
        return False
    return True

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_photo(file):
    if not  allowed_file(file.filename):
        flash('Oops! Allowed image types are -> png, jpg, jpeg, gif', 'error')
        return False
    data = file.read()
    if len(data) > 1000*1024:
        flash('Oops! Too large a photo.', 'error')
        return False
    return True

def validate_comment(title, comment, recipe_id):
    if len(title) > 150:
        flash('Oops! Title is too long', 'error')
        return False
    if len(comment) > 500:
        flash('Oops! Commment is too long', 'error')
        return False
    if not recipes.get(recipe_id):
        flash('Oops! The recipe does not exist anymore!', 'error')
        return False
    return True
