from sqlalchemy import create_engine
from datetime import datetime, timezone
import requests
import pandas as pd

BASE_URL = "https://api.openweathermap.org/data/2.5/group?"

API_KEY = open('api_key', 'r').read().strip()

CITY_ID = 'id=703448,2643743,756135,3088171'

UNITS = "metric"

url = BASE_URL + CITY_ID + "&units=" + UNITS + "&appid=" + API_KEY

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
df_expanded = pd.concat([
    weather_data,
    pd.json_normalize(weather_data['meta.coord']).add_prefix('city.'),
    pd.json_normalize(weather_data['meta.sys']).add_prefix('city.'),
    pd.json_normalize(weather_data['meta.main']).add_prefix('main.'),
    pd.json_normalize(weather_data['meta.wind']).add_prefix('wind.'),
    pd.json_normalize(weather_data['meta.clouds']).add_prefix('clouds.')
], axis=1).drop(columns=['meta.coord', 'meta.sys', 'meta.main', 'meta.wind', 'meta.clouds'])

df_expanded.rename(columns={
    'city.sunrise': 'sunrise',
    'city.sunset': 'sunset'
}, inplace=True)

#Convert weather date to UTC time
df_expanded['dt'] = df_expanded['dt'].apply(lambda x: datetime.fromtimestamp(x, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))

# Convert sys.sunrise and sys.sunset to UTC time
df_expanded['sunrise'] = df_expanded['sunrise'].apply(lambda x: datetime.fromtimestamp(x, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
df_expanded['sunset'] = df_expanded['sunset'].apply(lambda x: datetime.fromtimestamp(x, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))


# Replace dots in column names with underscores
df_expanded.columns = df_expanded.columns.str.replace('.', '_', regex=False)

# Insert data to STG layer
dbschema = 'stg'
engine = create_engine('postgresql+psycopg2://etl:postgres@localhost:5432/dwh',
                       connect_args={'options': '-csearch_path={}'.format(dbschema)})

df_expanded.to_sql('stg_weather_data', engine, if_exists='append', index=False)