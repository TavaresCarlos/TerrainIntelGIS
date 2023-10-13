# Use a imagem base
FROM python:3.6
# Configurar o diretório de trabalho
WORKDIR /backend
# Copiar os arquivos do aplicativo para o contêiner
COPY . /backend
# Instalar as dependências do aplicativo
RUN pip install -r requirements.txt
# Expor a porta em que o aplicativo é executado
EXPOSE 3000
# Comando para iniciar o aplicativo
CMD ["python", "./sistema/backend/flaskr/server.py"]
