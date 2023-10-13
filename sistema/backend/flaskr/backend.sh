#!/bin/sh

#Não pode ~saltar linha depois do último comando

pip install --upgrade pip

pip install flask
pip install -U flask-cors

pip install numpy
pip install pandas

pip install pyjwt
pip install -U Flask-SQLAlchemy

pip install scikit-learn
pip install pyclustering

pip install reportlab

pip install mysql-connector-python

python -u server.py