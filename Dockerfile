FROM python:3.9

RUN pip3 install tweepy python-time kafka-python python-dotenv

ADD .env .

ADD api_developer_authentication.py .

ADD main.py .

CMD ["python", "./main.py"]
