from flask import Flask, render_template, request
from create_graph import create_graph, get_beautiful_soup
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
        response = get_beautiful_soup(thinker)
        # If Wikipedia raises DisambiguationError, shows you the options
        if isinstance(response, list):
            return render_template('main.html', disambiguation_options=response.options)
        else: 
            title, graph = create_graph(response)
            link_name = title.replace(" ", "_")
            graph.write_svg(f"./static/img/{link_name}.svg")
            with open(f"./static/img/{link_name}.svg") as svg:
                return render_template('action.html', thinker=title, svg=svg.read())
    except Exception as e:
        print(e)
        return render_template('main.html', error="Sorry 🤷‍♂️, I don't know them. Try someone else!")

if __name__ == '__main__':
    app.run()