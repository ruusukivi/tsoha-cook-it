from flask import render_template, redirect, request, url_for, flash
from app import app
import users
import recipes
import validation

@app.route('/')
def index():
    latest = recipes.get_all()
    types = recipes.get_types()
    return render_template('index.html', recipes=latest, types=types)

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
    return render_template('error.html', message='Sign up failed.')

@app.route('/profile/<string:profilename>',methods=['GET'])
def get_profile(profilename):
    if request.method == 'GET':
        profile_recipes = recipes.get_recipes(profilename)
        return render_template('profile.html', profile_recipes=profile_recipes,
        profilename=profilename)
    return render_template('error.html', message='User was not found.')

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
        likes = recipes.get_likes(recipe_id)
        return render_template('recipe.html', recipe=recipe, likes=likes)
    return render_template('error.html', message='Recipe was not found.')

@app.route('/recipe/like',methods=['POST'])
def like_recipe():
    if request.method == 'POST':
        users.check_csrf()
        recipe_id = request.form['recipe_id']
        if recipes.like_recipe(recipe_id):
            return redirect(url_for('get_recipe', recipe_id=recipe_id))
    return render_template('error.html', message='Something went sideways.')

@app.route('/recipe/delete',methods=['POST'])
def delete_recipe():
    recipe_id = request.form['recipe_id']
    if request.method == 'POST':
        users.check_csrf()
        if recipes.delete_recipe(recipe_id):
            flash('Done! You have now deleted the recipe.')
            return redirect("/")
    flash('You can delete only you own recipes.', error)
    return redirect(url_for('get_recipe', recipe=recipe))
