from sqlalchemy import create_engine
import requests
import pandas as pd

BASE_URL = "https://api.openweathermap.org/data/2.5/group?"
API_KEY = open('api_key', 'r').read()
CITY_ID = 'id=703448,2643743,756135,3088171'
UNITS = "metric"

url = BASE_URL + CITY_ID + "&units=" + UNITS + "&appid" + API_KEY

data = requests.get(url).json()

# Further normalize the 'weather' field to extract its data into separate columns
weather_data = pd.json_normalize(data['list'], 'weather', ['coord', 'sys', 'main', 'visibility', 'wind', 'clouds', 'dt', 'id', 'name'], meta_prefix='meta.')

# Flatten the DataFrame
df_expanded = pd.concat([
    weather_data,
    pd.json_normalize(weather_data['meta.coord']).add_prefix('coord.'),
    pd.json_normalize(weather_data['meta.sys']).add_prefix('sys.'),
    pd.json_normalize(weather_data['meta.main']).add_prefix('main.'),
    pd.json_normalize(weather_data['meta.wind']).add_prefix('wind.'),
    pd.json_normalize(weather_data['meta.clouds']).add_prefix('clouds.')
], axis=1).drop(columns=['meta.coord', 'meta.sys', 'meta.main', 'meta.wind', 'meta.clouds'])

#print(df_expanded)

dbschema='public'
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres',
                       connect_args={'options': '-csearch_path={}'.format(dbschema)})

df_expanded.to_sql('weather', engine, if_exists='append', index=False)
