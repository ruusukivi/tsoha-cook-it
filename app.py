from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    words=["word1","word2", "word3"]
    return render_template("index.html", message="Welcome!",items=words)

@app.route("/page1")
def page1():
    return "Page1!"


@app.route("/page2")
def page2():
    return "Page2!"

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])

@app.route("/test")
def test():
    content = " "
    for i in range(100):
        content += str(i+1) + " "
    return content

@app.route("/page/<int:id>")
def page(id):
    return "Page: " + str(id)