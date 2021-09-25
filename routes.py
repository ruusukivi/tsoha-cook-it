from flask import render_template, redirect, request, url_for
from app import app
import users
import recipes

@app.route('/')
def index():
    newest = recipes.get_all()
    types = recipes.get_types()
    return render_template('index.html', recipes=newest, types = types)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            return redirect('/')
    return render_template('login.html', message='Please check username and password')

@app.route('/logout')
def logout():
    users.logout()
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
        if len(password) < 9:
            return render_template('signup.html', message='Oops! Password is too short')
        if password != password2:
            return render_template('signup.html', message='Oops! Passwords do not match')
        if users.signup(username, password, profilename):
            return render_template('login.html', message='Sign up done! Please log in')
    return render_template('error.html', message='Sign up failed.')

@app.route('/newrecipe',methods=['GET', 'POST'])
def addrecipe():
    if request.method == 'GET':
        types = recipes.get_types()
        return render_template('newrecipe.html', types = types)
    if request.method == 'POST':
        users.check_csrf()
        name = request.form['name']
        description = request.form['description']
        typeid = request.form['typeid']
        steps = request.form['steps']
        ingredients = request.form['ingredients']
        if recipes.add_recipe(name, description, typeid, steps, ingredients):
            return redirect('/')
    return render_template('error.html',
    message='Adding the recipe failed. Please fill all fields.')

@app.route('/recipe/<int:recipe_id>',methods=['GET'])
def get_recipe(recipe_id):
    if request.method == 'GET':
        recipe = recipes.get(recipe_id)
        likes = recipes.get_likes(recipe_id)
        return render_template('recipe.html', recipe = recipe, likes = likes)
    return render_template('error.html', message='Recipe was not found.')

@app.route('/recipe/like',methods=['POST'])
def like_recipe():
    if request.method == 'POST':
        users.check_csrf()
        recipe_id = request.form['recipe_id']
        if recipes.like_recipe(recipe_id):
            return redirect(url_for('get_recipe', recipe_id = recipe_id))
    return render_template('error.html', message='Something went sideways.')

@app.route('/recipe/delete',methods=['POST'])
def delete_recipe():
    if request.method == 'POST':
        users.check_csrf()
        recipe_id = request.form['recipe_id']
        print(recipe_id)
        if recipes.delete_recipe(recipe_id):
            return redirect("/")
    return render_template('error.html', message='You can delete only you own recipes.')
