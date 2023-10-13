FROM python:3.6

WORKDIR /backend

COPY . /backend

RUN bash ./flaskr/backend.sh

EXPOSE 3000

CMD ["python", "server.py"]
