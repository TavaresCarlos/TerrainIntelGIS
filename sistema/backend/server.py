#pip install flask
#pip install -U flask-cors

from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def home():
	return ('Hello World, cross-origin')

app.run('0.0.0.0')
