import pandas as pd
from pathlib import Path
import json
from datetime import datetime

# Шлях до розпакованого файлу
tmp_dir = Path(__file__).resolve().parent.parent / 'tmp/owm_city'
json_file = tmp_dir / 'city.list.json'

def transform_owm_city():
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)  # Завантажуємо JSON як Python-об'єкт (list[dict])

    df = pd.json_normalize(data)  # Трансформуємо в DataFrame
    df.columns = df.columns.str.replace('.', '_', regex=False)
    df["load_date"] = pd.to_datetime(datetime.today())
    return df
if __name__ == "__main__":
    transform_owm_city()