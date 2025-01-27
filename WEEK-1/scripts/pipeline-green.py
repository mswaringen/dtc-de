import sys
from time import time
import pandas as pd
from sqlalchemy import create_engine, text
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """convert datetime columns to datetime"""
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    return df

def get_database_url() -> str:
    """get database url from environment variables"""
    db_host = os.getenv('DB_HOST', 'pg-database')
    db_url = f'postgresql://root:root@{db_host}:5432/ny_taxi'
    return db_url

def drop_table_if_exists(engine, table_name: str):
    """drop table if exists"""
    with engine.connect() as connection:
        connection.execute(text(f'DROP TABLE IF EXISTS {table_name}'))
        connection.commit()
    logging.info(f"Dropped table {table_name} if it existed")

def main(file_path: str, chunksize: int=50000):
    # read csv into an iterator in chunks
    df_iter = pd.read_csv(file_path, iterator=True, chunksize=chunksize)

    # create engine to connect to postgres
    engine = create_engine(get_database_url())

    # drop the exisiting table if it exists
    drop_table_if_exists(engine, "green_taxi_data")

    # Get the first chunk to create the table
    df_head = next(df_iter)
    df_head = clean_data(df_head)

    # Create table with header only
    df_head.head(0).to_sql(name="green_taxi_data", con=engine, if_exists="replace")
    logging.info("Created table with header only")

    # Insert the first chunk
    df_head.to_sql(name="green_taxi_data", con=engine, if_exists="append", method="multi")
    logging.info("Inserted the first chunk")

    # Insert the remaining chunks
    try:
        while True:
            t_start = time()

            df = next(df_iter)
            df = clean_data(df)
            df.to_sql(name="green_taxi_data", con=engine, if_exists="append", method="multi")

            t_end = time()
            logging.info(f"Inserted another chunk, took {t_end - t_start:.2f} seconds")
    except StopIteration:
        logging.info("Finished loading data into iterator.")

    except Exception as e:
        logging.error(f"Error inserting data: {e}")

    logging.info("Finished inserting data")
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python pipeline.py <input_file>")
        sys.exit(1)
    else:
        filename =  sys.argv[1]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, "data", filename)

        logging.info(f"Opening {file_path}")
        main(file_path)

        logging.info("Pipeline completed successfully")