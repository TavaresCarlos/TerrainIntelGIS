#Se um atributo tem outlier, remove o atributo todo da base

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
import statistics

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

		global arquivo
		arquivo = pd.read_csv(file)

		#List with name of all cities
		global cities_name
		cities_name =  get_cities_name(arquivo)
	
		global dicts
		dicts = arquivo.to_dict()

		return render_template('features.html', content=dicts)
		
		#File to tests
		#return render_template('treinamento.html', content=str(arquivo))


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

		array_cluster_cities = cluster_cities_generate(number_k, cities_name, cluster)
		array_cluster_properties = cluster_properties_generate(number_k, file_float_tratament, cluster)
		array_cluster_statistics = cluster_statistics_generate(number_k, array_cluster_properties)
		
		#GRÁFICO LATERAL: GRÁFICO X E Y COM OS CLUSTERS GERADOS APÓS O PCA

		g = [
			cluster,
			[number_k],
			array_cluster_cities,
			array_cluster_properties,
			array_cluster_statistics,
			list(features_selecteds)
		]

		return render_template('display-map.html', content=list(g))
		
		#File to tests
		#return render_template('treinamento.html', content=array_cluster_statistics)

#
def cluster_statistics_generate(number_k, array_cluster_properties):
	array_cluster = []

	for array_value in array_cluster_properties:
		aux = []
		for j in array_value:
			'''
			O valor adicionado em j define qual a propriedade que eu estou considerando
			j=0 - primeira propriedade selecionda
			j=1 - segunda propriedade selecionda
			E assim por diante

			VALIDAR OS VALORES DE MÉDIA RETORNADOS
			A PROPRIEDADE MANGUEZAL GERA UM VALOR A MAIS NO NUMERO DE CLUSTERS
			'''
			#aux.append(j[0])
			for i in j:
				aux.append(i)

		#array_cluster.append(statistics.mean(aux))
		#array_cluster.append(statistics.variance(aux))
		
		#Median from each cluster generate
		array_cluster.append(statistics.median(aux))

	return array_cluster


#Associate properties values with your clustering generate
def cluster_properties_generate(number_k, file_float_tratament, cluster):
	array_cluster = []
	for i in range(number_k):
		aux = []
		array_cluster.append(aux)
	cont = 0
	for i in cluster:
		array_cluster[i].append(file_float_tratament[cont])
		cont = cont + 1

	pos = 0
	for i in array_cluster:
		if(len(i) == 0):
			del array_cluster[pos]
		pos += 1

	return array_cluster

#Associate each city with your clustering generate
def cluster_cities_generate(number_k, cities_name, cluster):
	array_cluster = []
	for i in range(number_k):
		aux = []
		array_cluster.append(aux)

	cont = 0
	for i in cluster:
		array_cluster[i].append(cities_name[cont])
		cont = cont + 1

	pos = 0
	for i in array_cluster:
		if(len(i) == 0):
			del array_cluster[pos]
		pos += 1

	return array_cluster

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
#Clustering algorithms
def k_means():
def affinity_propagation:
'''

#Função que retorna o ponto central de todos os municípios do arquivo de treinamento
def map_municipio_cluster(nome_municipios, cluster):
	return dict(zip(nome_municipios, cluster))

#Function return a list with name of all cities from the .csv file
def get_cities_name(training_file):
	names = []
	for city in training_file['Nome do Municipio']:
		names.append(city)

	return names

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

def k_means(file, number_k):
	kmeans = KMeans(n_clusters = number_k, random_state = 0)
	cluster = kmeans.fit_predict(file)
	return list(cluster)

app.run(host="0.0.0.0", port=3000, debug = True)

'''
IMPORTANTE: Posso trocar todos os NaN pelo valor 0 ?? (estudar isso)
Remover valores NaN dos arquivos
'''
