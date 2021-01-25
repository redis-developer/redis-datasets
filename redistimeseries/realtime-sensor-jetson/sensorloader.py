import bme680
import time
import datetime
import csv
import argparse
import redis


print("""read-sensor.py - Displays temperature, pressure, humidity, and gas.
Press Ctrl+C to exit!
""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented
# out, if desired.

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int,
                    help="redis instance port", default=6379)
parser.add_argument(
    "--password", type=int, help="redis instance password", default=None
)
parser.add_argument(
    "--verbose", help="enable verbose output", action="store_true")
parser.add_argument("--host", type=str,
                    help="redis instance host", default="127.0.0.1")


args = parser.parse_args()

# redis setup
redis_obj = redis.Redis(host=args.host, port=args.port, password=args.password)
temperature_key = "ts:temperature"
pressure_key = "ts:pressure"
humidity_key = "ts:humidity"

print('\n\nPolling:')
try:
    while True:
        if not sensor.get_sensor_data():
            print('Can not access sensor data')
            continue

        output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity)

        if not sensor.data.heat_stable:
            print('Heat unstable: ' + output)
            continue

        print('{0},{1} Ohms'.format(
            output,
            sensor.data.gas_resistance))

        date = datetime.datetime.now()
        timestamp = int(date.timestamp() * 1000)

        # Create pipeline
        pipe = redis_obj.pipeline()

        pipe.execute_command(
            "ts.add", temperature_key, timestamp, sensor.data.temperature
        )

        pipe.execute_command(
            "ts.add", pressure_key, timestamp, sensor.data.pressure
        )

        pipe.execute_command("ts.add", humidity_key,
                             timestamp, sensor.data.humidity)

        # Execute pipeline
        pipe.execute()

        time.sleep(1)

except KeyboardInterrupt:
    pass
