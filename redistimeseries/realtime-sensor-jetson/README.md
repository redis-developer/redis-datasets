## Loading BME680 Sensor data directly into RedisTimeSeries(over Redis Enterprise Cloud)

![My Image](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/realtime-sensor-jetson/Screenshot%202021-01-04%20at%2011.29.15%20PM.png)

### Pre-requisite

- Jetson Nano 4GB/2GB Model/Raspberry Pi/Arduino
- Redis Enterprise Cloud Account configured with Subscription and Account
   - Endpoint Required
   - Password
   - Port
- Install Python on your Jetson board
   
   
### Installing Required Modules

1. Install bme680 python module


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
1611046300.446452 [0 122.179.79.106:53715] "info" "server"
1611046300.450452 [0 122.179.79.106:53717] "info" "stats"
1611046300.450452 [0 122.179.79.106:53716] "info" "clients"
1611046300.486452 [0 122.179.79.106:53714] "info" "memory"
1611046300.486452 [0 122.179.79.106:53713] "info" "server"
1611046300.494452 [0 122.179.79.106:53715] "info" "memory"
1611046300.498452 [0 122.179.79.106:53717] "info" "commandstats"
1611046300.522452 [0 122.179.79.106:53716] "dbsize"
1611046301.498452 [0 122.179.79.106:53714] "info" "memory"
1611046301.498452 [0 122.179.79.106:53713] "info" "server"
1611046301.498452 [0 122.179.79.106:53715] "info" "server"
1611046301.498452 [0 122.179.79.106:53716] "info" "clients"
1611046301.498452 [0 122.179.79.106:53717] "info" "stats"
1611046301.554452 [0 122.179.79.106:53714] "info" "memory"
1611046301.562452 [0 122.179.79.106:53717] "info" "commandstats"
1611046301.566452 [0 122.179.79.106:53716] "dbsize"
1611046301.598452 [0 70.167.220.160:43390] "MULTI"
1611046301.598452 [0 70.167.220.160:43390] "ts.add" "ts:temperature" "1611046301456" "29.26"
1611046301.598452 [0 70.167.220.160:43390] "ts.add" "ts:pressure" "1611046301456" "952.03"
1611046301.598452 [0 70.167.220.160:43390] "ts.add" "ts:humidity" "1611046301456" "13.804"
1611046301.598452 [0 70.167.220.160:43390] "EXEC"
1611046302.458452 [0 122.179.79.106:53715] "info" "server"
1611046302.462452 [0 122.179.79.106:53714] "info" "memory"
1611046302.462452 [0 122.179.79.106:53716] "info" "server"
1611046302.462452 [0 122.179.79.106:53713] "info" "stats"
1611046302.462452 [0 122.179.79.106:53717] "info" "clients"
```

## Plotting it over Grafana


It will be exciting to plot the sensor data over Grafana. To implement this, run the below command either on your laptop or on your preferable IoT device:=


```
$ docker run -d -e  "GF_INSTALL_PLUGINS=redis-datasource" -p 3000:3000 grafana/grafana
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
