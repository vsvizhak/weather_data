import pandas as pd
from sqlalchemy import create_engine
from etl.transform.trg_geonames import filter_large_cities  # імпортуй звідти, де зберігається твоя функція

def load_to_db(df: pd.DataFrame):
    # Параметри підключення
    db_user = "твій_користувач"
    db_password = "твій_пароль"
    db_host = "localhost"
    db_port = "5432"
    db_name = "твоя_база"
    table_name = "geonames_cities"

    # Створюємо engine
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    # Завантажуємо в базу
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Дані успішно записано в таблицю {table_name}")

if __name__ == "__main__":
    df_cities = filter_large_cities(min_population=100_000)
    load_to_db(df_cities)
