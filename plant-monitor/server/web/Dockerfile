FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask gunicorn
COPY app.py .
COPY templates templates
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "app:app"]
