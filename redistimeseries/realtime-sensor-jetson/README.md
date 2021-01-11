## Loading BME680 Sensor data directly into RedisTimeSeries(over Redis Enterprise Cloud)

![My Image](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/realtime-sensor-jetson/Screenshot%202021-01-04%20at%2011.29.15%20PM.png)

### Pre-requisite

- Jetson Nano 4GB/2GB Model/Raspberry Pi/Arduino
- Redis Enterprise Cloud Account configured with Subscription and Account
   - Endpoint Required
   - Password
   - Port
- Install Python3 on your Jetson board
   
   
### Installing Required Modules

1. Installing bme680 python module


```
$ pip3 install bme680
Password:
Collecting bme680
  Downloading bme680-1.0.5-py3-none-any.whl (11 kB)
Installing collected packages: bme680
Successfully installed bme680-1.0.5
```

2. Install smbus python module 

```
pip3 install smbus
```

### Setting up Jetson Nano with BME680

 
#### Wiring

![My Image](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/realtime-sensor-jetson/Screenshot%202021-01-05%20at%208.47.38%20AM.png)

## Cloning the Repository

```
git clone https://github.com/redis-developer/redis-datasets
cd redis-datasets/redistimeseries/realtime-sensor-jetson
```


## Running the script

- Change the entries as per your Redis Enterprise Cloud account 

```
python3 sensorloader.py --host <endpoint> --port <port>  --password <password> 
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

## Plotting it over Grafana


It will be exciting to plot the sensor data over Grafana. To implement this, run the below command either on your laptop or on your preferable IoT device:=


```
$ docker run -d -e "GF_INSTALL_PLUGINS=redis-app" -e "GF_INSTALL_PLUGINS=redis-datasource" -p 3000:3000 grafana/grafana
```


Ensure that Grafana container is up and running as shown below:

```
$ docker ps
CONTAINER ID   IMAGE             COMMAND     CREATED         STATUS         PORTS                    NAMES
38148d69f114   grafana/grafana   "/run.sh"   5 seconds ago   Up 4 seconds   0.0.0.0:3000->3000/tcp   reverent_feynman
```



Open browser and point it to https://<IP_ADDRESS>:3000. Use “admin” as username and “admin” as password to login into Grafana dashboard.


Click on the “Data Sources” option on the left side of the Grafana dashboard to add data source. Search for “Redis” as shown below:



Supply the name, redis database endpoint, password and click on “Save & Test”. Ensure that it displays “Datasource updated”.


![My image](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/realtime-sensor-jetson/Screenshot%202021-01-09%20at%2010.54.18%20PM.png)
