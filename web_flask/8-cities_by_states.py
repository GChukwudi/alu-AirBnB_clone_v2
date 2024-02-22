#!/usr/bin/python3
"""
script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    """ close session """
    storage.close()


@app.route('/')
def cities_by_states():
    """ display a HTML page: (inside the tag BODY) """
    states = storage.all(State)
    sorted_stated = sorted(states, key=lambda k: k.name)

    return render_template('8-cities_by_states.html', states=sorted_stated)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
