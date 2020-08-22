## Creating

RedisTimeSeries does this indexing for you based on field value pairs (a.k.a labels) you can add to each time series, and use to filter at query time (a full list of these filters is available in our documentation). Here’s an example of creating a time series with two labels (sensor_id and area_id are the fields with values 2 and 32 respectively) and a retention window of 60,000 milliseconds:

    TS.CREATE temperature RETENTION 60000 LABELS sensor_id 2 area_id 32

```
TS.CREATE temperature:4:12 RETENTION 40 LABELS sensor_id 4 area_id 32
OK
TS.CREATE temperature:5:15 RETENTION 50 LABELS sensor_id 5 area_id 40
OK
TS.CREATE temperature:6:18 RETENTION 60 LABELS sensor_id 6 area_id 48
OK
```


## Adding


```
TS.ADD temperature:4:12 404505606707 30
TS.ADD temperature:4:12 404505606708 31
TS.ADD temperature:5:15 505606707808 50
TS.ADD temperature:5:15 505606707809 51
TS.ADD temperature:6:18 606707808909 60
TS.ADD temperature:6:18 606707808910 61
```

## Last Sample

```
TS.GET temperature:5:15
1) (integer) 505606707809
```

```
TS.GET temperature:4:12
1) (integer) 404505606708
2) 31
```

## using Filters

```
TS.MGET FILTER area_id=32
1) 1) "temperature:4:12"
   2) (empty array)
   3) 1) (integer) 404505606708
      2) 31

```
## With Labels

```
 TS.MGET WITHLABELS FILTER area_id=32
1) 1) "temperature:4:12"
   2) 1) 1) "sensor_id"
         2) "4"
      2) 1) "area_id"
         2) "32"
   3) 1) (integer) 404505606708
      2) 31

 ```
 
 ## Query a range across one or multiple time-series


```
TS.RANGE temperature:5:15 505606707808 5056067070810
1) 1) (integer) 505606707809
   2) 51

```

```
TS.RANGE temperature:4:12 404505606707 404505606710
1) 1) (integer) 404505606707
   2) 30
2) 1) (integer) 404505606708
   2) 31
```






