#!/bin/sh
export FLASK_APP=./app/index.py
export MONGO_USER=arif
export MONGO_PASSWORD=zubkHKBWRyYMjKSS
. $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0