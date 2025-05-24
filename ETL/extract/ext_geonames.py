from pathlib import Path
import requests
import zipfile

# Створюємо шлях до директорії tmp (всередині etl)
tmp_dir = Path(__file__).resolve().parent.parent / 'tmp/geonames'
tmp_dir.mkdir(parents=True, exist_ok=True)  # Створюємо папку, якщо її немає

# Шлях до ZIP-файлу всередині tmp
zip_file_path = tmp_dir / 'cities15000.zip'


def download_geonames_data():
    url = "http://download.geonames.org/export/dump/cities15000.zip"

    # Завантаження ZIP-файлу
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(zip_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    print(f"Файл {zip_file_path} завантажено успішно!")


def extract_zip_file(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Файл {zip_file} розпаковано в {extract_to}")

if __name__ == "__main__":
    download_geonames_data()
    extract_zip_file(zip_file_path, tmp_dir)
