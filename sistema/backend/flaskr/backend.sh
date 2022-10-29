#!/bin/sh

pip install flask
pip install -U flask-cors

pip install numpy
pip install pandas

pip install pyjwt
pip install psycopg2
pip install -U Flask-SQLAlchemy

pip install scikit-learn
pip install pyclustering

python -u server.py
