# Базовий імейдж
FROM prefecthq/prefect:2.11.5-python3.11

# Робоча директорія в контейнері
WORKDIR /opt/prefect/flows

# Скопіювати залежності
COPY requirements.txt ./

# Встановити їх
RUN pip install --no-cache-dir -r requirements.txt

# Скопіювати решту твого коду
COPY . .

# Опційно: можна одразу запускати Prefect server (якщо потрібен)
CMD ["prefect", "server", "start", "--host", "0.0.0.0"]
