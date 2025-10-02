FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

# Order service expects PRODUCT_SERVICE_URL env variable
CMD ["python", "app.py"]
