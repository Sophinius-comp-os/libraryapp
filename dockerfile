FROM python:3.10.0a7-alpine3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /django

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn librarymgmt.wsgi.wsgi:application --bind 0.0.0.0:8000

EXPOSE 8000
