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

from scipy import stats as sts
from sklearn.cluster import KMeans

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()

def home():
	df_2 = pd.read_csv('recursos-naturais-municipios.csv', on_bad_lines='skip')

	aux = tratamento(df_2)
	cluster = treinamento(aux)

	return str(cluster)

#Tratamento dos dados númericos do CAR
def tratamento(df_2):
	app = df_2['APP']
	superior_1800 = df_2['Altitude Superior 1800']
	consolidade = df_2['Consolidada']
	declividade_maior_45 = df_2['Declividade Maior 45']
	imoveis = df_2['Imoveis']
	pousio = df_2['Pousio']
	topo_morro = df_2['Topo de Morro']
	banhado = df_2['Banhado']
	borda_chapada = df_2['Borda Chapada']
	hidrografia = df_2['Hidrografia']
	manguezal = df_2['Manguezal']
	nascentes = df_2['Nascentes']
	reserva_legal = df_2['Reserva Legal']
	restinga = df_2['Restinga']
	servidao_administrativa = df_2['Servidão Administrativa']
	restrito = df_2['Restrito']
	vegetacao_nativa = df_2['Vegetação Nativa']
	vereda = df_2['Vereda']
	                           
	app_f = []
	superior_1800_f = []
	consolidade_f = []
	declividade_maior_45_f = []
	imoveis_f = []
	pousio_f = []
	topo_morro_f = []
	banhado_f = []
	borda_chapada_f = []
	hidrografia_f = []
	manguezal_f = []
	nascentes_f = []
	reserva_legal_f = []
	restinga_f = []
	servidao_administrativa_f = []
	restrito_f = []
	vegetacao_nativa_f = []
	vereda_f = []
	                           
	for i in app:
	    app_f.append(float(i))

	for i in superior_1800:
	    superior_1800_f.append(float(i))
	                           
	for i in consolidade:
	    consolidade_f.append(float(i))
	                           
	for i in declividade_maior_45:
	    declividade_maior_45_f.append(float(i))
	                           
	for i in imoveis:
	    imoveis_f.append(float(i))
	                           
	for i in pousio:
	    pousio_f.append(float(i))
	                           
	for i in topo_morro:
	    topo_morro_f.append(float(i))
	                           
	for i in banhado:
	    banhado_f.append(float(i))
	                           
	for i in borda_chapada:
	    borda_chapada_f.append(float(i))
	                           
	for i in hidrografia:
	    hidrografia_f.append(float(i))
	                           
	for i in manguezal:
	    manguezal_f.append(float(i))
	                           
	for i in nascentes:
	    nascentes_f.append(float(i))
	                           
	for i in reserva_legal:
	    reserva_legal_f.append(float(i))
	                           
	for i in restinga:
	    restinga_f.append(float(i))
	                           
	for i in servidao_administrativa:
	   servidao_administrativa_f.append(float(i))
	                           
	for i in restrito:
	    restrito_f.append(float(i))
	                           
	for i in vegetacao_nativa:
	    vegetacao_nativa_f.append(float(i))
	                           
	for i in vereda:
	    vereda_f.append(float(i))

	aux = []

	for i in range(len(df_2)):
	    t = []
	    t.append(app_f[i])
	    t.append(superior_1800_f[i])
	    t.append(consolidade_f[i])
	    t.append(declividade_maior_45_f[i])
	    t.append(imoveis_f[i])
	    t.append(pousio_f[i])
	    t.append(topo_morro_f[i])
	    t.append(banhado_f[i])
	    t.append(borda_chapada_f[i])
	    t.append(hidrografia_f[i])
	    t.append(manguezal_f[i])
	    t.append(nascentes_f[i])
	    t.append(reserva_legal_f[i])
	    t.append(restinga_f[i])
	    t.append(servidao_administrativa_f[i])
	    t.append(restrito_f[i])
	    t.append(vegetacao_nativa_f[i])
	    t.append(vereda_f[i]) 
	    aux.append(t)

	return aux

def treinamento(aux):
	kmeans = KMeans(n_clusters = 5, random_state = 0)
	cluster = kmeans.fit_predict(aux)
	return cluster

app.run(host="localhost", port=int("3000"))
