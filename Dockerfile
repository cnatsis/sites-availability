FROM python:3.8-slim-buster
LABEL maintainer="Christos Natsis"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]