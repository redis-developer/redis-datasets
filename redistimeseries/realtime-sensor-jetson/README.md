## Loading BME680 Sensor data directly into RedisTimeSeries(over Redis Enterprise Cloud)

![My Image](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/realtime-sensor-jetson/Screenshot%202021-01-04%20at%2011.29.15%20PM.png)

### Pre-requisite

- Jetson Nano 4GB/2GB Model
- Redis Enterprise Cloud Account configured with Subscription and Account
   - Endpoint Required
   - Password
   - Port

### Setting up Jetson Nano with BME680

 
#### Wiring

- Connect the Jetson Nano 3.3V power pin to Vin
- Connect the Jetson Nano GND pin to GND
- Connect the Jetson Nano SDA (#3) pin to the BME280 SDI
- Connect the Jetson Nano SCL (#5) pin to to the BME280 SCK


![My Image](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/realtime-sensor-jetson/Screenshot%202021-01-04%20at%2011.38.59%20PM.png)

## Cloning the Repository

```
git clone https://github.com/redis-developer/redis-datasets
cd redis-datasets/redistimeseries/realtime-sensor-jetson
```


## Running the script

- Change the entries as per your Redis Enterprise Cloud account 

```
python3 sensorloader.py --host <Redis Enterprise Cloud host> --port <port>  --password <password> 
```

- For Example

```
ajeetraina@Ajeets-MacBook-Pro ~ % redis-cli -h redis-12929.c212.ap-south-1-1.ec2.cloud.redislabs.com -p 12929
redis-12929.c212.ap-south-1-1.ec2.cloud.redislabs.com:12929> auth <password>
OK
redis-12929.c212.ap-south-1-1.ec2.cloud.redislabs.com:12929> monitor
OK
1609595834.025344 [0 70.167.220.160:52138] "ts.add" "ts:temperature" "1609595833" "29.43"
1609595834.309343 [0 70.167.220.160:52138] "ts.add" "ts:pressure" "1609595833" "968.11"
1609595834.581343 [0 70.167.220.160:52138] "ts.add" "ts:humidity" "1609595833" "14.589"
1609595835.873342 [0 70.167.220.160:52138] "ts.add" "ts:temperature" "1609595835" "29.42"
1609595836.153342 [0 70.167.220.160:52138] "ts.add" "ts:pressure" "1609595835" "968.11"
1609595836.433341 [0 70.167.220.160:52138] "ts.add" "ts:humidity" "1609595835" "14.583"
1609595837.725340 [0 70.167.220.160:52138] "ts.add" "ts:temperature" "1609595837" "29.42"
1609595838.005340 [0 70.167.220.160:52138] "ts.add" "ts:pressure" "1609595837" "968.11"
1609595838.285340 [0 70.167.220.160:52138] "ts.add" "ts:humidity" "1609595837" "14.579"
```

