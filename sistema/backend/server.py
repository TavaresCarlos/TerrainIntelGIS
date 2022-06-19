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

        arquivo = pd.read_csv(file, on_bad_lines='skip')
 
        nome_municipios = get_nome_municipios(arquivo)

       	'''
 		#Determina o centroide de todos os clusters
        pontosCentrais = get_pontos_centrais(arquivo)
        '''

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

#Função que retorna o ponto central de todos os municípios do arquivo de treinamento
def map_municipio_cluster(nome_municipios, cluster):
	return dict(zip(nome_municipios, cluster))

#Função que retorna uma lista com o nome de todos os municipios do arquivo de treinamento
def get_nome_municipios(arquivo_treinamento):
	nome_munic = []
	for i in arquivo_treinamento['Nome do Municipio']:
		nome_munic.append(i)

	return nome_munic

#Função que calcula o valor ideal de k para o algoritmo KMeans
def gerando_valor_k(df_2):
	valores_silhouette_scores = []

	for i in range(2,15):
	    km = KMeans(n_clusters = i, random_state = 42, init = 'k-means++')
	    km.fit_predict(df_2)
	    score = silhouette_score(df_2, km.labels_, metric='euclidean')
	    
	    x = []
	    x.append(i)
	    x.append(score)
	    valores_silhouette_scores.append(x)

	cont = 2
	diferenca = []
	for i in range(len(valores_silhouette_scores)+1):
	    if i+1 < len(valores_silhouette_scores):
	        delta = []
	        cont = cont + 1
	        delta.append(cont)
	        #Subtração dos valores de score i+1 e i
	        delta.append(valores_silhouette_scores[i][1]-valores_silhouette_scores[i+1][1])
	        diferenca.append(delta)
	
	#Ordena o vetor de forma decrescente com base na diferença calculada
	valorK = sorted(diferenca, key=lambda diferenca: diferenca[1], reverse=True)
	
	#O maior valor da diferença sempre vai ser o primeiro do vetor
	#print(valorK[0])
	
	return valorK[0]

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

def treinamento(aux, k):
	kmeans = KMeans(n_clusters = k, random_state = 0)
	cluster = kmeans.fit_predict(aux)
	return cluster

app.run(host="localhost", port=3000, debug = True)

'''
IMPORTANTE: Posso trocar todos os NaN pelo valor 0 ?? (estudar isso)
Remover valores NaN dos arquivos
'''
