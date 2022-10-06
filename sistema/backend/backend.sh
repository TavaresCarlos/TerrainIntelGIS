#!/bin/sh

pip install flask
pip install -U flask-cors
pip install pandas
pip install scikit-learn
pip install pyclustering

python -u server.py
