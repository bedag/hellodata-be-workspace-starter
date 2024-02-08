FROM python:3.10-slim

RUN mkdir -p /opt/airflow/airflow_home/dags/
#create directory for file-mount
RUN mkdir -p /mnt/pvc/
RUN mkdir -p /usr/src/dbt/
RUN mkdir -p /usr/src/dbt-docs/


COPY ../src/dags-functions/requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
#requirements.txt is an example - please add your own dependencies here)
RUN pip install -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app

# Set ENV variable 
COPY deployment/env /usr/src/app/.env
COPY utils/set_envs.sh /usr/src/app/set_envs.sh
RUN chmod +x set_envs.sh

# Copy the script into the container
COPY src/duckdb/query_duckdb.py /usr/src/app/

# python helpers for DAGs 
COPY ../src/dags-functions/* /usr/src/app/
# Copy your airflow DAGs which will be copied into bussiness domain Airflow (These DAGs will be executed by Airflow)
COPY ../src/dags/airflow/dags/* /opt/airflow/airflow_home/dags/
COPY ../src/dbt/ /usr/src/dbt/

# long-running process to keep the # Define the entrypoint script
ENTRYPOINT ["./set_envs.sh"]

# Long-running process to keep the container running, should be specified as CMD if you're using an ENTRYPOINT script
CMD ["tail", "-f", "/dev/null"]
