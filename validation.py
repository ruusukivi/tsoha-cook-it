from flask import flash
import users

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
