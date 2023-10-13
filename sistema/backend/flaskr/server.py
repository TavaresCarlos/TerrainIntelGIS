#Se um atributo tem outlier, remove o atributo todo da base

#pip install flask
#pip install -U flask-cors

'''
Flask =
render_template =
jsonify =
send_file = 
'''

from flask import Flask, request, render_template, jsonify, send_file, url_for, make_response
from flask_cors import CORS, cross_origin

#Libraries and packages to data manipulation
import pandas as pd
import numpy as np
import json
import statistics
import math
import mysql.connector

#Libraries and packages to authentication
#from flask_sqlalchemy import SQLAlchemy
#import jwt

#Libraries and packages to data mining
from sklearn import preprocessing
from scipy import stats as sts
from sklearn.cluster import KMeans
from werkzeug.utils import secure_filename
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import minmax_scale

import csv

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Pasta que vai ser salvo o histórico de arquivos upados
app.config["UPLOAD_FOLDER"] = "static/"

#@app.route('/')
@cross_origin()

@app.route('/')
def upload_file():
	return render_template('home.html')

@app.route('/index', methods = ['POST'])
def index():
	conexao = mysql.connector.connect(
	    host="mysql26-farm10.kinghost.net",
	    user="webgisbrasil",
	    password="lineage123",
	    database="webgisbrasil"
	)

	login = request.form['email']
	senha = request.form['senha']

	cursor = conexao.cursor()

	n = ''
	s = ''
	e = ''

	if cursor:
	    selecionar = "SELECT name, senha, email FROM user WHERE email = %s" 
	    dados = (login)

	    cursor.execute(selecionar, (dados,))
	    resultados = cursor.fetchall()

	    for linha in resultados:
	    	n, s, e = linha

	cursor.close()
	conexao.close()

	if "entrar" in request.form:
		if e == login and s == senha:
			return render_template('index.html')
		else:
			return render_template('home.html')
	elif "esqueceuSenha" in request.form:
		return render_template('cadastro.html')
	elif "cadastro" in request.form:
		return render_template('cadastro.html')

@app.route('/features', methods = ['GET', 'POST'])
def upload():
	if request.method == 'POST':
		#Import the .csv file
		f = request.files['file']

		filename = secure_filename(f.filename)
		f.save(app.config['UPLOAD_FOLDER'] + filename)
		file = open(app.config['UPLOAD_FOLDER'] + filename,"r")

		global informarK
		informarK = request.form['informarK']
		
		if informarK == 'sim':
			global valorK
			valorK = int(request.form['valorK'])

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

		global number_k

		#Defining the k number for the k-means
		if informarK == 'sim':
			number_k = valorK
		else:
			number_k = defining_k_value(file_float_tratament)

		#K-Means
		cluster = k_means(file_float_tratament, number_k)

		global array_cluster_cities
		global array_cluster_statistics
		global array_cluster_properties

		array_cluster_cities = cluster_cities_generate(number_k, cities_name, cluster[0])
		array_cluster_properties = cluster_properties_generate(number_k, file_float_tratament, cluster[0])

		
		#GRÁFICO LATERAL: GRÁFICO X E Y COM OS CLUSTERS GERADOS APÓS O PCA

		l = [list(x) for x in list(cluster[2])]

		g1 = {
			"agrupamentos": list(cluster[0]),
			"centroide": list(cluster[1]),
			"centroide_normalizado": l,
			"numero_grupos": number_k,
			"nome_cidades": cities_name,
			"cidades_agrupamentos": list(array_cluster_cities),
			"valores_brutos": array_cluster_properties,
			"propriedades_selecionadas": list(features_selecteds)
		}

		return render_template('display-map.html', name=g1)
		
		#File to tests
		#return render_template('treinamento.html', content=array_cluster_statistics)

@app.route('/gerarRelatorio', methods = ['POST'])
def gerarRelatorio():
	with open('./relatorio.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(['Agrupamento', 'Média', 'Cidades'])

		for i in range(number_k):
			writer.writerow([i,array_cluster_statistics[i], array_cluster_cities[i]])

	return "ok"

@app.route('/cadastro', methods = ['POST'])
def cadastro():
	conexao = mysql.connector.connect(
	    host="mysql26-farm10.kinghost.net",
	    user="webgisbrasil",
	    password="lineage123",
	    database="webgisbrasil"
	)

	nome = request.form['nome']
	email = request.form['email']
	senha = request.form['senha']

	cursor = conexao.cursor()

	if cursor:
	    inserir = "INSERT INTO user (name, email, senha) VALUES (%s, %s, %s)"
	    dados = (nome, email, senha)

	    cursor.execute(inserir, dados)
	    conexao.commit()

	cursor.close()
	conexao.close()

	return render_template('cadastro.html')

@app.route('/logout', methods = ['POST'])
def sair():
	return render_template('home.html')

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
			#aux.append(j)
			for i in j:
				aux.append(i)

		#array_cluster.append(statistics.median(aux))
		array_cluster.append(statistics.pstdev(aux))

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


#Função que retorna o ponto central de todos os municípios do arquivo de treinamento
def map_municipio_cluster(nome_municipios, cluster):
	return dict(zip(nome_municipios, cluster))

#Function return a list with name of all cities from the .csv file
def get_cities_name(training_file):
	names = []
	for city in training_file['Nome do Municipio']:
		names.append(city)

	return names

def distanciaRetaPontos(diferencas):
	dist = []

	#Calculo da reta
	x0 = diferencas[0][0]
	y0 = diferencas[0][1]

	x1 = diferencas[len(diferencas)-1][0]
	y1 = diferencas[len(diferencas)-1][1]

	for i in diferencas:
		aux = []
		x = i[0]
		y = i[1]

		numerador = abs((y1-y0)*x - (x1-x0)*y - y1*x0)
		denominador = math.sqrt((y1-y0)**2 + (x1-x0)**2)
		d = numerador/denominador
		aux.append(x)
		aux.append(y)
		dist.append(aux)

	maior = sorted(dist, key=lambda d: d[1], reverse=True)

	return maior[0]

def defining_k_value(file):
	quantidade = 2
	valores = []

	for vez in range(quantidade):
		inicio = 2
		fim = 10
		inercia = []

		for i in range(inicio, fim):
			kmeans = KMeans(n_clusters = i)
			kmeans.fit(file)
			inercia.append(kmeans.inertia_)

		diferente = []
		for j in range(2, len(inercia)):
			if j+1 != len(inercia):
				t = []
				m = inercia[j] - inercia[j+1]
				t.append(j+1)
				t.append(m)
				diferente.append(t)

		k = distanciaRetaPontos(diferente)

		valorK = k
		valores.append(valorK[0])

	return statistics.mode(valores)

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
	centroide = kmeans.cluster_centers_


	#Agrupamento com os dados normalizados
	file_norm = minmax_scale(file)
	kmeans_norm = KMeans(n_clusters = number_k, random_state = 0)
	cluster_norm = kmeans_norm.fit_predict(file_norm)
	
	#centroid_minmax = kmeans_norm.cluster_centers_

	centroid_minmax = minmax_scale(centroide)

	return list(cluster), centroide, centroid_minmax

app.run(host="0.0.0.0", port=3000, debug = True)

'''
IMPORTANTE: Posso trocar todos os NaN pelo valor 0 ?? (estudar isso)
Remover valores NaN dos arquivos
'''
