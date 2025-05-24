from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/group"
CITY_IDS = ['703448', '2643743', '756135', '3088171']
UNITS = "metric"

def build_url():
    city_param = ",".join(CITY_IDS)
    return f"{BASE_URL}?id={city_param}&units={UNITS}&appid={api_key}"

def load_data():
    url = build_url()
    print(f"Requesting: {url}")
    response = requests.get(url)
    response.raise_for_status()  # зловить помилки, якщо 4xx / 5xx
    return response.json()