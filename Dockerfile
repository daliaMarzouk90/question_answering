FROM python:3.9.6

WORKDIR /var/app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5050
CMD exec gunicorn -w 2 -b :5050 --timeout=0 config:app
