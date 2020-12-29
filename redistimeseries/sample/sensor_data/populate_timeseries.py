import redis
import click
import time
import random


@click.command()
@click.option('--host', default="localhost", help='redis host.')
@click.option('--port', type=click.INT, default=6379, help='redis port.')
@click.option('--sensor-id', type=click.INT, help='sensor id')
def main(host, port, sensor_id):
    r = redis.Redis(host=host, port=port)

    while True:
        r.execute_command('TS.ADD', 'temperature:%d' % (sensor_id,), '*', random.randrange(10, 20),
                          'LABELS', '__name__', 'temperature', 'sensor', sensor_id)
        r.execute_command('TS.ADD', 'humidity:%d' % (sensor_id,), '*', random.randrange(70, 80),
                          'LABELS', '__name__', 'humidity', 'sensor', sensor_id)
        time.sleep(1)


if __name__ == '__main__':
    main()
