from flask import Flask, render_template, request
from create_graph import create_graph
app = Flask(__name__)

@app.route('/')
@app.route('/thinker/<name>')
def hello_world(name=None):
    return render_template("main.html", name=name)
@app.route("/action", methods = ['POST'])
def action():
    thinker = request.form.get('thinker')
    create_graph(thinker)
    thinker_underscore = thinker.replace(" ", "_")
    return render_template('action.html', thinker=thinker, thinker_underscore=thinker_underscore)