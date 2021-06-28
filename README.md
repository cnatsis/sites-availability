# Sites Availability Tool

This is the Python application that performs website checks periodically and collects the HTTP response time, status
code returned, as well as optionally checking the returned page contents for a regexp pattern that is expected to be
found on the page.

The application produces metrics to Apache Kafka topics and sinks to a PostgreSQL database using the Kafka Consumer API.

Both Kafka and PostgreSQL are deployed using [Aiven](https://aiven.io/) managed services.

## Table of Contents

* [Run](#run)
    * [Local](#local)
    * [Docker](#docker)
* [Packaging](#packaging)
* [Tests](#tests)

## Run

### Local

1. In order the application to run, a set of environment variables must be set in the [credentials.env](credentials.env)
   file.

Those variables are:

| Name              | Example Value        | Description                           |
|-------------------|----------------------|---------------------------------------|
| AIVEN_TOKEN       | your_token           | Aiven API Authentication Token        |
| AIVEN_PROJECT     | your_project_name    | Aiven Project Name                    |
| AIVEN_API_URL     | https://api.aiven.io | Aiven API URL                         |
| AIVEN_KAFKA_NAME  | kafka_instance_name  | Aiven Kafka service name              |
| AIVEN_PG_NAME     | pg_instance_name     | Aiven PostgreSQL service name         |
| AIVEN_KAFKA_CLOUD | azure-westeurope     | Cloud Provider for Kafka service      |
| AIVEN_KAFKA_PLAN  | business-4           | Service Plan for Kafka service        |
| AIVEN_PG_CLOUD    | azure-westeurope     | Cloud Provider for PostgreSQL service |
| AIVEN_PG_PLAN     | startup-4            | Service Plan for PostgreSQL service   |

Also, the `PRODUCER_INTERVAL` variable used to periodically check the sites is set automatically and defaults to five
(5) seconds.

2. Install requirements

(Optional) Create a virtual environment

Install Python packages from [requirements.txt](requirements.txt) file.

```bash
pip3 install -r requirements
```

3. Edit sites to check list

The file [sites.txt](conf/sites.txt) contains a list of sites to check, along with a regex pattern that fetches content
from the website.

Each valid row of the file must contain a site url and optionally, if a regex pattern needs to be checked, a space
character and the regex pattern.

Valid examples:

```text
https://www.cnn.com <title>(.*?)</title>
https://www.google.com
```

4. To run the application, run the commands:

```bash
source credentials.env
python3 -m src
```

If you are using PyCharm, just run `src/__main__.py` normally and pass environment variables using
the `Edit Configuration` panel.

### Docker

In order to run the application using the Docker image (see [Packaging](#packaging) for build instructions), simply run
the following command.

```bash
docker-compose up -d

# Check logs 
docker logs sites-availability -f
```

In case you need to change the list of sites to check, please follow the commands:

```bash
mkdir conf
nano conf/sites.txt # Fill in your content
docker-compose up -d
```

## Packaging

The application is packaged using Docker.

To create a Docker image of the application use the following command. This command will create a Docker
image `sites-availability:latest`. Make sure your current working directory contains the [Dockerfile](Dockerfile) and
the [docker-compose](docker-compose.yml) files.

```bash
# Build only the image with the following
docker build . -t sites-availability:latest

# or... build and run
docker-compose up --build
```

## Tests

In order to run the tests, it is assumed a Kafka and a PostgreSQL service is up and in RUNNING state, and the correct
environment variables must be set (Check [#1](#local)).

```bash
source credentials.env
python3 -m unittest tests/ApplicationTests.py
```





