from flask import Flask, render_template, request
from create_graph import create_graph
import wikipedia
import sys
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("main.html")
@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/thinker/<name>')
def hello_world(name=None):
    return render_template("main.html")
@app.route("/action", methods = ['POST'])
def action():
    thinker = request.form.get('thinker')
    try:
        thinker_underscore, title = create_graph(thinker)
        with open("static/img/%s.svg" % thinker_underscore) as svg:
            return render_template('action.html', thinker=title, svg=svg.read())
    except wikipedia.exceptions.DisambiguationError as e:
        return render_template('main.html', disambiguation_options=e.options)
    except Exception as e:
        return render_template('main.html', error="Sorry 🤷‍♂️, I don't know them. Try someone else!")

if __name__ == '__main__':
    app.run()