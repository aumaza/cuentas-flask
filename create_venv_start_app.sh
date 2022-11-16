#!/bin/bash

python3 -m venv venv
. venv/bin/activate
pip install flask flask-sqlalchemy flask-login
python3 main.py