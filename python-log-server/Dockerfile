FROM python:2.7-alpine

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
COPY templates /app/templates
COPY js /app/js

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python app.py