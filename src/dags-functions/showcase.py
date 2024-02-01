import os
import sys
import pandas as pd

# from datetime import datetime, timedelta
from datetime import timedelta
import re

from rdfpandas.graph import to_dataframe
import rdflib
import pandas as pd
import psycopg2
import argparse

POSTGRES_URL = os.getenv("POSTGRES_URL", "localhost")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "sspaeti")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "host.docker.internal")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "tierstatistik")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DRIVER_CLASS_NAME = os.getenv(
    "POSTGRES_DRIVER_CLASS_NAME", "org.postgresql.Driver"
)
SQL_SCHEMA_NAME = "tierstatistik_lzn."


def data_download():
    print("Downloading data...")

    def snake_case(s: str):
        """
        Converts a string to snake_case

        :param str s: The string to convert to snake case
        :return: Input string converted to snake case
        :rtype: str

        Example input:  "get2HTTPResponse123Code_Style _  Manace- LIKE"
        Example output: "get2_http_response123_code_style_manace_like"
        """
        pattern = re.compile("((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))")
        # a = "_".join( s.replace('-', ' ').replace('_', ' ').replace("'", " ").replace(',', ' ').replace('(', ' ').replace(')', ' ').split() )
        a = re.sub("[^A-Za-z0-9_]", "", s)
        return pattern.sub(r"_\1", a).lower()

    def df_breed_melt(df_data):
        df_data_new = df_data.melt(
            id_vars=["Year", "Month"], var_name="breed", value_name="n_animals"
        )
        return df_data_new

    sys.path.append("/mnt/*/")
    g = rdflib.Graph()
    g.parse("https://tierstatistik.identitas.ch/tierstatistik.rdf", format="xml")
    df = to_dataframe(g)

    data_path = "/mnt/pvc/"

    for index in df.index:
        file_url = index
        if "csv" in index:
            file_name_csv = index
            df_data = pd.read_csv(file_name_csv, sep=";", index_col=None, skiprows=1)

            if "breeds" in index:
                df_data = df_breed_melt(df_data)

            df_data.rename(columns=lambda x: snake_case(x), inplace=True)
            df_data.to_csv(
                data_path + os.path.basename(file_name_csv).split("/")[-1],
                index=False,
            )
            print(f"File downloaded and processed: {file_name_csv}")

            # DEBUG: only for testing only one CSV
            # break


def create_tables():
    print("Create tables...")
    conn_str = f"dbname='{POSTGRES_DATABASE}' user='{POSTGRES_USERNAME}' host='{POSTGRES_HOST}' password='{POSTGRES_PASSWORD}' port='{POSTGRES_PORT}'"
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    data_path = "/mnt/pvc/"

    # loop through csv only
    csv_files = [file for file in os.listdir(data_path) if file.endswith(".csv")]

    for file in csv_files:
        file_path_csv = os.path.join(data_path, file)
        print(file_path_csv)

        df_data = pd.read_csv(file_path_csv)
        sql_table_name = (
            SQL_SCHEMA_NAME
            + os.path.basename(file_path_csv)
            .split("/")[-1]
            .split(".")[0]
            .replace("-", "_")
            .lower()
        )
        sql_column_name_type = ""

        for column in df_data.columns:
            if sql_column_name_type == "":
                sql_column_name_type += f""""{column}" TEXT"""
            else:
                sql_column_name_type += f""", "{column}" TEXT"""

        cur.execute(f"""DROP TABLE IF EXISTS {sql_table_name};""")
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {sql_table_name} ( {sql_column_name_type} );"""
        )
        conn.commit()


def insert_data():
    print("Insert tables...")
    conn_str = f"dbname='{POSTGRES_DATABASE}' user='{POSTGRES_USERNAME}' host='{POSTGRES_HOST}' password='{POSTGRES_PASSWORD}' port='{POSTGRES_PORT}'"
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    data_path = "/mnt/pvc/"

    # loop through csv only
    csv_files = [file for file in os.listdir(data_path) if file.endswith(".csv")]

    for file in csv_files:
        file_path_csv = os.path.join(data_path, file)
        sql_table_name = (
            SQL_SCHEMA_NAME
            + os.path.basename(file_path_csv)
            .split("/")[-1]
            .split(".")[0]
            .replace("-", "_")
            .lower()
        )
        with open(file_path_csv, "r") as file:
            cur.copy_expert(
                f"""COPY {sql_table_name} FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'""",
                file,
            )
        conn.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run specific functions in the script."
    )
    parser.add_argument(
        "--data_download", action="store_true", help="Run the data_download function"
    )

    parser.add_argument(
        "--create_tables", action="store_true", help="Run the create_tables function"
    )

    parser.add_argument(
        "--insert_data", action="store_true", help="Run the insert_data function"
    )

    args = parser.parse_args()

    if args.data_download:
        data_download()
    if args.create_tables:
        create_tables()
    if args.insert_data:
        insert_data()
