#!/bin/sh
export FLASK_APP=./app/index.py
. $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0