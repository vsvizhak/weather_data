from pathlib import Path
import requests
import gzip
import shutil

# Створюємо шлях до директорії tmp (всередині etl)
tmp_dir = Path(__file__).resolve().parent.parent / 'tmp/owm_city'
tmp_dir.mkdir(parents=True, exist_ok=True)  # Створюємо папку, якщо її немає

# Шлях до ZIP-файлу всередині tmp
gz_file_path = tmp_dir / 'city.list.json.gz'


def download_owm_city_data():
    url = "https://bulk.openweathermap.org/sample/city.list.json.gz"

    # Завантаження ZIP-файлу
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(gz_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Файл {gz_file_path} завантажено успішно!")


def extract_gz_file(zip_file, extract_to):
    with gzip.open(gz_file_path, 'rb') as f_in:
        with open(f"{tmp_dir}/city.list.json", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

if __name__ == "__main__":
    download_owm_city_data()
    extract_gz_file(gz_file_path, tmp_dir)