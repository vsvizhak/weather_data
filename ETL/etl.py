from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
import oracledb
from datetime import datetime, timezone
import requests
import pandas as pd
import logging

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")
db_creds = os.getenv("DB_URL")

def load_data():
    BASE_URL = "https://api.openweathermap.org/data/2.5/group?"
    CITY_ID = 'id=703448,2643743,756135,3088171'
    UNITS = "metric"
    url = BASE_URL + CITY_ID + "&units=" + UNITS + "&appid=" + api_key

    data = requests.get(url).json()

    # Normalize 'weather' field and expand it into separate columns
    weather_data = pd.json_normalize(
        data['list'],
        record_path='weather',
        meta=['coord', 'sys', 'main', 'visibility', 'wind', 'clouds', 'dt', 'id', 'name'],
        meta_prefix='meta.',
        record_prefix='weather.'
    )

    weather_data.rename(columns={
        'meta.dt': 'dt',
        'meta.id': 'city.id',
        'meta.name': 'city.name',
        'meta.visibility': 'visibility'
    }, inplace=True)

    # Flatten the DataFrame by combining nested JSON fields
    df = pd.concat([
        weather_data,
        pd.json_normalize(weather_data['meta.coord']).add_prefix('city.'),
        pd.json_normalize(weather_data['meta.sys']).add_prefix('city.'),
        pd.json_normalize(weather_data['meta.main']).add_prefix('main.'),
        pd.json_normalize(weather_data['meta.wind']).add_prefix('wind.'),
        pd.json_normalize(weather_data['meta.clouds']).add_prefix('clouds.')
    ], axis=1).drop(columns=['meta.coord', 'meta.sys', 'meta.main', 'meta.wind', 'meta.clouds'])

    df.rename(columns={
        'city.sunrise': 'sunrise',
        'city.sunset': 'sunset'
    }, inplace=True)

    #Convert weather date to UTC time
    df['dt'] = df['dt'].apply(lambda x: datetime.fromtimestamp(x, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))

    # Convert sys.sunrise and sys.sunset to UTC time
    df['sunrise'] = df['sunrise'].apply(lambda x: datetime.fromtimestamp(x, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    df['sunset'] = df['sunset'].apply(lambda x: datetime.fromtimestamp(x, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))


    # Replace dots in column names with underscores
    df.columns = df.columns.str.replace('.', '_', regex=False)

    # Insert data to STG layer
    dbschema = 'stg'
    # engine = create_engine(db_creds,
    #                     connect_args={'options': '-csearch_path={}'.format(dbschema)})

    user = "ADMIN"
    password = "Qahehyreb573/"
    host = "adb.uk-london-1.oraclecloud.com"
    port = 1522
    service_name = "g641e06b314e952_dwh_high.adb.oraclecloud.com"
    dsn = "dwh_high"



    engine = create_engine(
        f"oracle+oracledb://{user}:{password}@{dsn}",
        connect_args={
            "config_dir": "/Users/vasyl/study/weather_data/DB_APP/Wallet_DWH",  # <== твій шлях
            "wallet_location": "/Users/vasyl/study/weather_data/DB_APP/Wallet_DWH",  # іноді треба теж
            "wallet_password": "Qahehyreb573/"  # якщо wallet без пароля


    }
    )

    with engine.begin() as conn:
        result = conn.execute(text("INSERT INTO stg.weather_data_loads DEFAULT VALUES RETURNING load_id, load_date"))
        load_id, load_date = result.fetchone()
        print(f"Load ID: {load_id}, Load Date: {load_date}")
        
    df['load_id'] = load_id
    df.to_sql('weather_data', engine, schema='stg', if_exists='append', index=False)

if __name__ == "__main__":
    load_data()


