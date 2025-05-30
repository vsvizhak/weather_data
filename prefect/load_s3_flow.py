from dotenv import load_dotenv
import requests
import os
import boto3
from datetime import datetime
from botocore.client import Config
from prefect import flow, task, get_run_logger


load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")

s3 = boto3.client(
    's3',
    endpoint_url=os.getenv("ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

BUCKET_NAME = 'weatherdata'


@task
def fetch_weather_data():
    logger = get_run_logger()
    BASE_URL = "https://api.openweathermap.org/data/2.5/group?"
    CITY_ID = 'id=703448,2643743,756135,3088171'
    UNITS = "metric"
    url = BASE_URL + CITY_ID + "&units=" + UNITS + "&appid=" + api_key
    logger.info("Starting data load from OpenWeather API")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        logger.info("Successfully fetched data from OpenWeather API")
        return response.raw
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        raise


@task
def ensure_bucket_exists():
    logger = get_run_logger()
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
        logger.info(f"Bucket '{BUCKET_NAME}' exists")
    except s3.exceptions.ClientError:
        logger.warning(f"Bucket '{BUCKET_NAME}' not found, creating...")
        s3.create_bucket(Bucket=BUCKET_NAME)
        logger.info(f"Bucket '{BUCKET_NAME}' created")


@task
def upload_to_s3(file_obj):
    logger = get_run_logger()
    now = datetime.now()
    filename = now.strftime("owm_%Y%m%d_%H%M%S.json")
    file_path = f'data/{filename}'

    try:
        s3.upload_fileobj(file_obj, BUCKET_NAME, file_path, ExtraArgs={'ContentType': 'application/json'})
        logger.info(f"Uploaded data to bucket '{BUCKET_NAME}' at '{file_path}'")
    except Exception as e:
        logger.error(f"Failed to upload file to S3: {e}")
        raise


@flow(name="Load Weather Data")
def load_s3_flow():
    ensure_bucket_exists()
    data_stream = fetch_weather_data()
    upload_to_s3(data_stream)


if __name__ == "__main__":
    load_s3_flow()
