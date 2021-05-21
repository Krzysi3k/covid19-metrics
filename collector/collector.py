import time
import csv
from datetime import datetime
import requests
from influxdb import InfluxDBClient

INFLUX_CONTAINER = 'influxdb'
DB_NAME = 'covid-19'

def get_data():
    url = 'https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv'
    r = requests.get(url)
    content = r.content.decode('utf-8').split('\n')
    reader = list(csv.reader(content))
    payload = []
    for line in reader[1:(len(reader) -2)]:
        payload.append({
            'measurement': 'covid19',
            'tags': {
                'date': line[0],
                'country': line[1]
            },
            'fields': {
                'confirmed': int(line[2]),
                'recovered': int(line[3]),
                'deaths': int(line[4]),
                'currently_infected': int(line[2]) - int(line[3]) - int(line[4]),
            },
            'time': int(datetime.strptime(line[0], '%Y-%m-%d').timestamp())
        })

    return payload


if __name__ == '__main__':
    # warmup time for influxdb
    time.sleep(60)
    t = time.time()
    payload = get_data()
    print(f'data generated in: {round((time.time() - t), 2)} seconds')
    t = time.time()
    client = InfluxDBClient(host=INFLUX_CONTAINER, port=8086, database=DB_NAME)
    client.create_database('covid-19')
    client.write_points(payload, time_precision='s')
    print(f'data inserted in: {round((time.time() - t), 2)} seconds')