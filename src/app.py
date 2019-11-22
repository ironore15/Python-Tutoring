from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return 'My First Webpage'

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/user/<name>')
def show_user(name):
    return 'Hello ' + name

@app.route('/template')
def template():
    return render_template('index.html')

@app.route('/hello/<name>')
def hello_user(name):
    return render_template('hello.html', username=name)

app.run()