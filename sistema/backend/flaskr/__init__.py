from flask import Flask
import server

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Pasta que vai ser salvo o histórico de arquivos upados
app.config["UPLOAD_FOLDER"] = "static/"

app.run(host="0.0.0.0", port=3000, debug = True)