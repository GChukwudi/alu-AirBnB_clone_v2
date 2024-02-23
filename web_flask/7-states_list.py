#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """teardown_appcontext"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """states_list"""
    states = storage.all(State)
    sort = sorted(states.values(), key=lambda k: k.name)
    return render_template('states_list.html', states=sort)


@app.route('/')
def hello_world():
    """hello world route"""
    return 'Hello World!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
