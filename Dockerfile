FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV LISTEN_PORT 3001

EXPOSE 3001

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app