FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY calculator.py .
COPY static ./static

ENV PORT=5000
EXPOSE 5000

CMD ["sh", "-c", "uvicorn calculator:app --host 0.0.0.0 --port ${PORT}"]