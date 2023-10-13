FROM python:3.6

WORKDIR /backend

COPY . /backend

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "server.py"]
