#pip install flask
#pip install -U flask-cors

'''
Flask =
render_template =
jsonify =
send_file = 
'''

from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS, cross_origin
import pandas as pd
import json

from sklearn import preprocessing

from scipy import stats as sts
from sklearn.cluster import KMeans

from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["UPLOAD_FOLDER"] = "static/"

#@app.route('/')
@cross_origin()

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")

        df_2 = pd.read_csv(file, on_bad_lines='skip')

        tratamento_dados_categoricos(df_2)
        aux = tratamento(df_2)
        
        #n_cluster = gerando_valor_k(df_2)
        #cluster = list(treinamento(aux, n_cluster))

        cluster = list(treinamento(aux))
        return jsonify(cluster=str(cluster))
        
        return jsonify(cluster=str(aux))
        
    return render_template('content.html', content=content) 


'''
def home():
	df_2 = pd.read_csv('recursos-naturais-municipios.csv', on_bad_lines='skip')

	aux = tratamento(df_2)
	cluster = treinamento(aux)

	return str(cluster)

'''

def tratamento_dados_categoricos(df_2):
	#Modificando colunas string para número
	for i in df_2:
	    if df_2[i].dtype == 'object':
	        le = preprocessing.LabelEncoder()
	        a = le.fit(df_2[i])
	        a = le.transform(df_2[i])
	        df_2[i] = a

#Tratamento dos dados númericos do CAR
def tratamento(df_2): 
	aux = [[]]
	j = 0
	for i in df_2:
	    #(implementar) Ignorar a primeira linha
	    if j != 0:
	        aux.append((df_2[i].to_numpy(dtype='float')))
	    j = j + 1

	teste = aux[1:]
	linhas = len(teste)
	colunas = len(teste[1])

	aux2 = [[]]

	for i in range(colunas):
	    t = []
	    for j in range(linhas):
	        t.append(teste[j][i])
	    aux2.append(t)

	dados = aux2[1:]

	return dados

def treinamento(aux):
	kmeans = KMeans(n_clusters = 5, random_state = 0)
	cluster = kmeans.fit_predict(aux)
	return cluster

app.run(host="localhost", port=3000, debug = True)

'''
IMPORTANTE: Posso trocar todos os NaN pelo valor 0 ?? (estudar isso)
'''
