#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    """Closes the session"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Displays an HTML page"""
    states = storage.all(State).values()
    sorted_
