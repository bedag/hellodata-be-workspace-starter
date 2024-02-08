FROM python:3.10-slim

RUN mkdir -p /opt/airflow/airflow_home/dags/
#create directory for file-mount
RUN mkdir -p /mnt/pvc/
RUN mkdir -p /usr/src/dbt/
RUN mkdir -p /usr/src/dbt-docs/

# Copy your airflow DAGs which will be copied into bussiness domain Airflow (These DAGs will be executed by Airflow)
COPY ../src/dags/airflow/dags/* /opt/airflow/airflow_home/dags/
COPY ../src/dbt/ /usr/src/dbt/

COPY ../src/dags-functions/requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
#requirements.txt is an example - please add your own dependencies here)
RUN pip install -r /usr/src/app/requirements.txt

# python helpers for DAGs 
COPY ../src/dags-functions/* /usr/src/app/
WORKDIR /usr/src/app

RUN pip install --upgrade pip
#requirements.txt is an example - please add your own dependencies here)
RUN pip install -r requirements.txt 

# Copy the script into the container
COPY src/duckdb/query_duckdb.py ./

# long-running process to keep the container running 
CMD tail -f /dev/null
