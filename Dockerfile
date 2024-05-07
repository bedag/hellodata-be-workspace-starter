FROM python:3.11-slim

# install vim for development
RUN apt-get update && apt-get install -y vim
# Create the workspace directory for devcontainers
RUN mkdir -p /workspace

RUN mkdir -p /opt/airflow/airflow_home/dags/

#create directory for file-mount
# RUN mkdir -p /mnt/pvc/
# RUN mkdir -p /usr/src/dbt/
# RUN mkdir -p /usr/src/dbt-docs/

COPY ./src/requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
#requirements.txt is an example - please add your own dependencies here)
RUN pip install -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app

# Copy the script into the container
COPY src/duckdb/query_duckdb.py /usr/src/app/

# the actual dag files
COPY ./src/dags/* /usr/src/app/dags/
# python helpers for DAGs
COPY ./src/dags-functions/* /usr/src/app/dags-functions/
# dbt models
COPY ./src/dbt/ /usr/src/app/dbt/
RUN (cd /usr/src/app/dbt/ && dbt deps)
