#pip install flask
#pip install -U flask-cors

'''
Flask =
render_template =
jsonify =
send_file = 
'''

from flask import Flask, request, render_template, jsonify, send_file,
from flask_cors import CORS, cross_origin
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def home():
	#Convertendo o .csv para .html
	data = pd.read_csv('recursos-naturais-municipios.csv', on_bad_lines='skip')
	return render_template('index.html', tables=[data.to_html()], titles=[''])

app.run(host="localhost", port=int("3000"))
