from flask import Flask, render_template, request
from create_graph import create_graph
import wikipedia
app = Flask(__name__)

@app.route('/')
@app.route('/thinker/<name>')
def hello_world(name=None):
    return render_template("main.html")
@app.route("/action", methods = ['POST'])
def action():
    thinker = request.form.get('thinker')
    try:
        thinker_underscore = create_graph(thinker)
        with open("static/img/%s.svg" % thinker_underscore) as svg:
            return render_template('action.html', thinker=thinker, svg=svg.read(), thinker_underscore=thinker_underscore)
    except wikipedia.exceptions.DisambiguationError as e:
        return render_template('main.html', disambiguation_options=e.options)
    except Exception as e:
        return render_template('main.html', error="Sorry, I don't them 🤷‍♂️")