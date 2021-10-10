from flask import render_template, redirect, request, url_for, flash, render_template_string
from app import app
import users
import recipes
import validation

@app.route('/')
def index():
    latest = recipes.get_all()
    popular = recipes.get_popular()
    commented = recipes.get_commented()
    types = recipes.get_types()
    return render_template('index.html', latest=latest, popular=popular, commented=commented,
    types=types)

#Signup, login, logout, granting admin rights

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        profilename = request.form['profilename']
        if not validation.validate_signup(password, password2, username, profilename):
            return redirect("/signup")
        if users.signup(username, password, profilename):
            flash('Sign up done! Please log in', 'success')
            return render_template('login.html')
    flash('Sign up failed. Please try again later.')
    return render_template('signup.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            flash('You are now logged in as ' + username + '!', 'success')
            return redirect('/')
    flash('Oops! Check username and password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    users.logout()
    flash('You are now logged out!', 'success')
    return redirect('/')

@app.route('/admin', methods=['POST'])
def grant_admin_rights():
    if request.method == 'POST':
        users.check_csrf()
        profilename = request.form['profilename']
        if users.update_admin_rights(profilename):
            flash('Admin rights granted!', 'success')
            return redirect(url_for('get_profile', profilename=profilename))
    flash('Admin rights could not be given.')
    return redirect(url_for('get_profile', profilename=profilename))

#Profile page

@app.route('/profile/<string:profilename>',methods=['GET'])
def get_profile(profilename):
    if request.method == 'GET':
        profile_recipes = recipes.get_recipes(profilename)
        profile_likes = recipes.get_profile_likes(profilename)
        profile_commented = recipes.get_profile_commented(profilename)
        return render_template('profile.html', latest=profile_recipes,
        popular=profile_likes, commented=profile_commented, profilename=profilename)
    return render_template('error.html', message='User was not found.')

#Recipe: new recipe, recipe page, deleting recipe

@app.route('/newrecipe',methods=['GET', 'POST'])
def addrecipe():
    form = request.form
    types = recipes.get_types()
    if request.method == 'GET':
        return render_template('newrecipe.html', types = types)
    if request.method == 'POST':
        users.check_csrf()
        name = form['name']
        description = form['description']
        typeid = form['typeid']
        steps = form['steps']
        ingredients = form['ingredients']
        if not validation.validate_recipe(name, description, typeid, steps, ingredients):
            return render_template("/newrecipe.html", form=form, types=types)
        if recipes.add_recipe(name, description, typeid, steps, ingredients):
            return redirect('/')
    flash('Adding the recipe failed. Please try again later.')
    return render_template("/newrecipe.html", form=form, types=types)

@app.route('/recipe/<int:recipe_id>',methods=['GET'])
def get_recipe(recipe_id):
    if request.method == 'GET':
        recipe = recipes.get(recipe_id)
        all_comments = recipes.get_comments(recipe_id)
        comments = recipes.get_comments_count(recipe_id)
        return render_template('recipe.html', recipe=recipe,
        all_comments=all_comments, comments=comments)
    return render_template('error.html', message='Recipe was not found.')

@app.route('/recipe/delete',methods=['POST'])
def delete_recipe():
    recipe_id = request.form['recipe_id']
    if request.method == 'POST':
        users.check_csrf()
        if recipes.delete_recipe(recipe_id):
            flash('Done! You have now deleted the recipe.')
            return redirect('/')
    flash('You can delete only you own recipes.', 'error')
    return redirect(url_for('get_recipe', recipe=recipe_id))

#Recipe likes and comments

@app.route('/recipe/like',methods=['POST'])
def like_recipe():
    if request.method == 'POST':
        users.check_csrf()
        recipe_id = request.form['recipe_id']
        if recipes.like_recipe(recipe_id):
            flash('Done! Your like is now updated ', 'success')
            return redirect(url_for('get_recipe', recipe_id=recipe_id))
    return render_template('error.html', message='Something went sideways.')

@app.route('/newcomment',methods=['POST'])
def addcomment():
    form = request.form
    title = form['title']
    comment = form['comment']
    recipe = form['recipe_id']
    if request.method == 'POST':
        users.check_csrf()
        if not validation.validate_comment(title, comment, recipe):
            return redirect(url_for('get_recipe', recipe_id=recipe))
        if recipes.add_comment(title, comment, recipe):
            return redirect(url_for('get_recipe', recipe_id=recipe))
    flash('Adding comment failed. Please try again later.', 'error')
    return redirect(url_for('get_recipe', recipe_id=recipe))

@app.route('/recipe/comment/delete',methods=['POST'])
def delete_comment():
    comment_id = request.form['id']
    recipe_id = request.form['recipe_id']
    if request.method == 'POST':
        users.check_csrf()
        if recipes.delete_comment(comment_id, recipe_id):
            flash('Done! You have now deleted the comment.')
            return redirect(url_for('get_recipe', recipe_id=recipe_id))
    flash('You can delete only your own comments.', 'error')
    return redirect(url_for('get_recipe', recipe_id=recipe_id))

# Search

@app.route('/search', methods=['GET', 'POST'])
def search():
    latest = recipes.get_all()
    types = recipes.get_types()
    if request.method == 'GET':
        return render_template('search.html', recipes=latest, types=types)
    if request.method == 'POST':
        searched_word = request.form['query']
        filtered_by_name = recipes.search_by_name(searched_word)
        return render_template('search_result.html', recipes=filtered_by_name, types=types)
    return render_template('search.html', recipes=latest, types=types)
