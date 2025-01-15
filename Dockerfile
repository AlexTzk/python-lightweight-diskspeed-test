FROM python:3.10-slim

WORKDIR /app

COPY disk_speed_flask.py /app

RUN pip install --no-cache-dir flask matplotlib

EXPOSE 5000

CMD ["python", "disk_speed_flask.py"]