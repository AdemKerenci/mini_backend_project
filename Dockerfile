FROM python:3.7.5-buster

COPY app app
COPY requirements.txt app/requirements.txt

WORKDIR app

RUN pip install -r requirements.txt

CMD python wsgi.py