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

@app.route('/features', methods = ['GET', 'POST'])
def upload():
	if request.method == 'POST':
		#Import the .csv file
		f = request.files['file']

		filename = secure_filename(f.filename)
		f.save(app.config['UPLOAD_FOLDER'] + filename)
		file = open(app.config['UPLOAD_FOLDER'] + filename,"r")

		arquivo = pd.read_csv(file)

		#List with name of all cities
		cities_name = get_cities_name(arquivo);
	
		global dicts
		dicts = arquivo.to_dict()

		#return render_template('features.html', content=dicts)
		
		#File to tests
		return render_template('treinamento.html', content=str(cities_name))


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
	if request.method == 'POST':
		features_selecteds = request.form

		list_of_features = []
		for value_of_feature in features_selecteds:
			list_of_features.append(dicts[value_of_feature])

		file_float_tratament = float_tratament(list_of_features)

		#Centroid of all clusters generated
		#Category data tratament
		#Numeric data tratament

		#Defining the k number for the k-means
		number_k = defining_k_value(file_float_tratament)

		#K-Means
		cluster = k_means(file_float_tratament, number_k)

		return render_template('display-map.html', content=list(cluster))
		
		#File to tests
		#return render_template('treinamento.html', content=str(number_k))

#OK
def float_tratament(list_of_features):
	new_list_of_atributes = []
	for feature_dict in list_of_features:
		aux = []
		for value in feature_dict.values():
			aux.append(float(value))
		new_list_of_atributes.append(aux)

	change_matrix = list(map(list, zip(*new_list_of_atributes)))

	return change_matrix

'''
@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
    	#Salva o aquivo upado dentro da pasta "/static" antes de realizar o treinamento
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")

        arquivo = pd.read_csv(file)
 
        nome_municipios = get_nome_municipios(arquivo)

 		#Determina o centroide de todos os clusters
        #pontosCentrais = get_pontos_centrais(arquivo)

        arquivo_tratamento_dados_categoricos = tratamento_dados_categoricos(arquivo)
        arquivo_tratamento_dados_numericos = tratamento(arquivo_tratamento_dados_categoricos)
        arquivo_tratado = arquivo_tratamento_dados_numericos

        n_cluster = gerando_valor_k(arquivo_tratado)
        cluster = list(treinamento(arquivo_tratado, n_cluster[0]))

        dicionario_municipio_cluster = map_municipio_cluster(nome_municipios, cluster)

        dados = jsonify(municípios=str(nome_municipios),n_cluster=str(n_cluster[0]),cluster=str(cluster))
        
        t = str(cluster)
        #return dados
        return render_template('content.html', content=t)
     
    return render_template('content.html', content=content)
'''

'''
#Clustering algorithms
def k_means():
def affinity_propagation:
'''

#Função que retorna o ponto central de todos os municípios do arquivo de treinamento
def map_municipio_cluster(nome_municipios, cluster):
	return dict(zip(nome_municipios, cluster))

#OK
#Function return a list with name of all cities from the .csv file
def get_cities_name(training_file):
	names = []
	for city in training_file['Nome do Municipio']:
		names.append(city)

	return names

#OK
#Define the ideal k value
#Use the Silhouette Score for determine the intra-cluster distance
def defining_k_value(file):
	values_silhouette_scores = []

	for i in range(2,15):
		#Use k-means auxiliary 
	    km = KMeans(n_clusters = i, random_state = 42, init = 'k-means++')
	    km.fit_predict(file)
	    score = silhouette_score(file, km.labels_, metric='euclidean')
	    
	    #Store the k value used in this iteraction and the score calculated
	    x = []
	    x.append(i)
	    x.append(score)
	    values_silhouette_scores.append(x)

	cont = 2
	variation = []

	for i in range(len(values_silhouette_scores)+1):
	    if i+1 < len(values_silhouette_scores):
	        delta = []
	        cont = cont + 1
	        delta.append(cont)

	        #Variation between of score values from i+1 and i
	        delta.append(values_silhouette_scores[i][1] - values_silhouette_scores[i+1][1])
	        variation.append(delta) 
	
	#Order this array decrescent using the variation defining
	valueK = sorted(variation, key=lambda variation: variation[1], reverse=True)
	
	#Return only the k value
	return valueK[0][0]

def tratamento_dados_categoricos(df_2):
	#Modificando colunas string para número
	for i in df_2:
	    if df_2[i].dtype == 'object':
	        le = preprocessing.LabelEncoder()
	        a = le.fit(df_2[i])
	        a = le.transform(df_2[i])
	        df_2[i] = a
	return df_2

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

#OK
def k_means(file, number_k):
	kmeans = KMeans(n_clusters = number_k, random_state = 0)
	cluster = kmeans.fit_predict(file)
	return cluster

app.run(host="0.0.0.0", port=3000, debug = True)

'''
IMPORTANTE: Posso trocar todos os NaN pelo valor 0 ?? (estudar isso)
Remover valores NaN dos arquivos
'''
