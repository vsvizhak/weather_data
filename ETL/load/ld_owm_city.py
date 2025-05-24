from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from ETL.transform.tf_owm_city import transform_owm_city

file_dir = Path(__file__).resolve().parent.parent / 'tmp/owm_city'

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_schema = 'stg'
table_name = 'stg_owm_city'
tmp_table = f"{table_name}_tmp"


def load_to_db(df: pd.DataFrame):
    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    with engine.begin() as connection:
        # Крок 1: Завантажити в допоміжну таблицю (створити, якщо її нема)
        df.to_sql(tmp_table, connection, schema=db_schema, if_exists="replace", index=False)

        #Крок 2: Очистити основну таблицю
        connection.execute(text(f"DELETE FROM {db_schema}.{table_name}"))

        # Крок 3: Перенести дані з tmp у основну
        connection.execute(text(f"""
            INSERT INTO {db_schema}.{table_name}
            SELECT * FROM {db_schema}.{tmp_table}
        """))

        # Крок 4 (необов’язковий): Очистити допоміжну таблицю
        connection.execute(text(f"DROP TABLE {db_schema}.{tmp_table}"))

    print("Дані успішно завантажено через tmp.")

if __name__ == "__main__":
    df_cities = transform_owm_city()
    load_to_db(df_cities)