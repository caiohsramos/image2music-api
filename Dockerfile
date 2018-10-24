FROM python:3.7

ENV LISTEN_PORT=$PORT

EXPOSE $PORT

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app /
CMD [ "python", "main.py" ]