FROM python:3.6-alpine

ADD . /work
WORKDIR /work

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
