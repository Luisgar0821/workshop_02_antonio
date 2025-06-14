FROM apache/airflow:2.8.1-python3.10

USER root
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev && apt-get clean

USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

