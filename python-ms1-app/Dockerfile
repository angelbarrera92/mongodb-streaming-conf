FROM python:2.7-alpine

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py

RUN pip install -r requirements.txt

EXPOSE 80

CMD python app.py