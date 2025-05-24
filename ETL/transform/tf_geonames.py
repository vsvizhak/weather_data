import pandas as pd
from pathlib import Path
from datetime import datetime

# Шлях до розпакованого файлу
tmp_dir = Path(__file__).resolve().parent.parent / 'tmp/geonames'
txt_file = tmp_dir / 'cities15000.txt'

# Колонки згідно з документацією GeoNames (можна скоротити список при потребі)
columns = [
    "geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude",
    "feature_class", "feature_code", "country_code", "cc2", "admin1_code",
    "admin2_code", "admin3_code", "admin4_code", "population", "elevation",
    "dem", "timezone", "modification_date"
]

def filter_large_cities(min_population=100_000):

    df = pd.read_csv(txt_file, sep='\t', header=None, names=columns, dtype={"population": int})

    # Фільтруємо великі міста
    df_large = df[df["population"] >= min_population].copy()

    #додаємо load_date
    df_large["load_date"] = pd.to_datetime(datetime.today())
    return df_large

if __name__ == "__main__":
    filter_large_cities()