FROM python:2.7-alpine

ADD . /work
WORKDIR /work

RUN pip install -r requirements.txt

CMD python main.py
