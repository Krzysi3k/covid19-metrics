FROM python:3.9.0-alpine
RUN pip install requests Influxdb
WORKDIR /app
COPY collector.py .
ENTRYPOINT [ "python", "collector.py" ]