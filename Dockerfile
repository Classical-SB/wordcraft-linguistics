FROM python:3.8

WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en
COPY src/ .
EXPOSE 80

CMD [ "python3", "./index.py" ]
