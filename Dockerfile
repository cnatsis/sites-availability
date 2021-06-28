FROM python:3.8-slim-buster
LABEL maintainer="Christos Natsis"

WORKDIR /app

RUN mkdir certs

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN ln -sf /usr/share/zoneinfo/Europe/Athens /etc/localtime
RUN echo "Europe/Europe" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

ENV PYTHONUNBUFFERED=1

CMD ["python3", "-m", "src"]