import os
import argparse
from time import time

import pandas as pd
from sqlalchemy import URL
from sqlalchemy import create_engine


def ingest_data(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table = params.table
    url = params.url
    file_downloaded = 'taxi_data.parquet'

    # download the file from the internet
    t_start = time()
    os.system(f'curl {url} --output {file_downloaded}')
    t_end = time()
    print(f'Total time taken to download the file: {t_end - t_start:.2f} seconds')

    # check if the file is downloaded
    if not os.path.exists(file_downloaded):
        print('File is not downloaded!')
        return

    df = pd.read_parquet(file_downloaded)
    print(df.shape)
    print(df.head())

    # Generate a DDL statement to create a table based on the columns in the dataframe
    connection_string = URL.create(drivername='postgresql', username=user, password=password,
                                   host=host, port=port, database=database)
    engine = create_engine(connection_string)
    print(pd.io.sql.get_schema(df, name=table))

    # create a table in the database
    df.head(n=0).to_sql(name=table, con=engine, if_exists='replace')
    # write data to a table
    t_start = time()
    df.to_sql(name=table, con=engine, if_exists='replace', chunksize=10000)
    t_end = time()
    print(f'Total time taken to write to the database: {t_end - t_start:.2f} seconds')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest New York taxi parquet data to Postgres')
    parser.add_argument('--user', required=True, help='Username for Postgres')
    parser.add_argument('--password', required=True, help='Password for Postgres')
    parser.add_argument('--host', required=True, help='Hostname for Postgres')
    parser.add_argument('--port', type=int, required=True, help='Port for Postgres')
    parser.add_argument('--database', required=True, help='Database name for Postgres')
    parser.add_argument('--table', required=True, help='Table name in Postgres to write data to')
    parser.add_argument('--url', required=True, help='URL of a parquet file to be downloaded')

    args = parser.parse_args()
    ingest_data(args)
