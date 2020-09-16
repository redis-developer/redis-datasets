# Redis Users Sample Dataset

This dataset contains users stored as Redis Hash.

This dataset could be used for:
* Redis Core
* RediSearch


### Movies

The movie hashes contain the following fields: 

* **`user:id`** : The key of the hash.
* **`first_name`** : First Name.
* **`last_name`** : Last name.
* **`email`** : email address.
* **`gender`** : Gender (male/female).
* **`ip_address`** : IP address.
* **`country`** : Country Name.
* **`country_code`** : Country Code.
* **`city`** : City of the user.
* **`longitude`** :  Longitude of the user. 
* **`latitude`** : Latitude of the user.
* **`last_login`** : EPOC time of the last login.


## Importing the dataset

The dataset files are  `redis-cli` scripts that you can import using the following command:


```
> redis-cli -h localhost -p 6379 < ./import_users.redis

```

Once done you can check some data:

```
> HMGET user:3333 first_name last_name city

1) "Myrlene"
2) "McGrane"
3) "Qinghu"
```


You can now use this dataset in your applications.

