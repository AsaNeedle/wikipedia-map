from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
@app.route('/thinker/<name>')
def hello_world(name=None):
    return render_template("main.html", name=name)