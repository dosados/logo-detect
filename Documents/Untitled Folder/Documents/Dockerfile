FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Обновление pip
RUN pip install --upgrade pip

# Создаем рабочую папку
WORKDIR /app

# Копируем файлы
COPY requirements.txt .
COPY app.py .
COPY weights/ ./weights/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт
EXPOSE 8000

# Запуск API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]