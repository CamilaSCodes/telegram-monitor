FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    EASYOCR_MODULE_PATH=/root/.EasyOCR

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "\
import easyocr; \
reader = easyocr.Reader(['en', 'pt'], gpu=False); \
print('✅ EasyOCR models preloaded successfully!') \
"

COPY . .

VOLUME ["/app"]

CMD ["python", "main.py"]
