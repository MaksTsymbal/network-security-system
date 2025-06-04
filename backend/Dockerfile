FROM python:3.10-slim

# Ставимо системні пакети для збірки psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gcc \
      libpq-dev \
      build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копіюємо requirements та одразу встановлюємо всі пакети
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо ваш код
COPY app/ ./app/

EXPOSE 8000

# Запуск
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]