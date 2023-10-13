FROM python:3.6

WORKDIR /backend

COPY . /backend

RUN bash ./backend.sh

EXPOSE 3000

CMD ["python", "server.py"]
