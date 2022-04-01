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

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Pasta que vai ser salvo o histórico de arquivos upados
app.config["UPLOAD_FOLDER"] = "static/"

#@app.route('/')
@cross_origin()

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
    	#Salva o aquivo upado dentro da pasta "/static" antes de realizar o treinamento
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")

        arquivo_treinamento = pd.read_csv(file, on_bad_lines='skip')

        tratamento_dados_categoricos(arquivo_treinamento)
        aux = tratamento(arquivo_treinamento)
        
        n_cluster = gerando_valor_k(arquivo_treinamento)
        cluster = list(treinamento(aux, n_cluster[0]))

        
        #cluster = list(treinamento(aux))
        return jsonify(cluster=str(cluster))
        
        #return jsonify(cluster=str(n_cluster[0]))
        
    return render_template('content.html', content=content) 

def gerando_valor_k(df_2):
	valores_silhouette_scores = []

	for i in range(2,15):
	    km = KMeans(n_clusters = i, random_state = 42)
	    km.fit_predict(df_2)
	    score = silhouette_score(df_2, km.labels_, metric='euclidean')
	    
	    x = []
	    x.append(i)
	    x.append(score)
	    valores_silhouette_scores.append(x)

	aux = [0,0]
	for i in range(len(valores_silhouette_scores)):
		if valores_silhouette_scores[i][1] > aux[1]:
			aux[0] = valores_silhouette_scores[i][0]
			aux[1] = valores_silhouette_scores[i][1]
	return aux

	#return valores_silhouette_scores

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

def treinamento(aux, k):
	kmeans = KMeans(n_clusters = k, random_state = 0)
	cluster = kmeans.fit_predict(aux)
	return cluster

app.run(host="localhost", port=3000, debug = True)

'''
IMPORTANTE: Posso trocar todos os NaN pelo valor 0 ?? (estudar isso)
'''
