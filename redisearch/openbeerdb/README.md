[![Actions Status](https://github.com/RediSearch/redisearch-beer/workflows/CI/badge.svg)](https://github.com/RediSearch/redisearch-beer/actions)

# rediseach-beer

Demo for RediSearch using the https://openbeerdb.com/ dataset.

## Running the Demo
To run the demo:
```
$ git clone https://github.com/RediSearch/redisearch-beer.git
$ cd redisearch-beer
$ docker-compose up
```
If something went wrong, you might need to force docker-compose to rebuild the containers
```
$ docker-compose up --force-recreate --build
```
Open a second terminal to connect to redis and explore the dataset:
```
$ redis-cli
```

## Example Queries
After the data is imported, you can query it using RediSearch. Some example commands:

Irish Ale and German Ale beers with ABV greater than 9%:
```
FT.SEARCH beerIdx "@category:Irish Ale|German Ale @abv:[9 inf]"
```
All beers with ABV higher than 5% but lower than 6%:
```
FT.SEARCH beerIdx "@abv:[5 6]"
```
Breweries in a 10km radius of the coordinates of Chicago, IL USA:
```
FT.SEARCH breweryIdx "@location:[-87.623177 41.881832 10 km]"
```

## Frontend
There is a rudimentary flask front end to show search functionality. To access the UI, point your web browser at http://localhost:5000/

## Notes
- The beers are added to the RediSearch index weighted by ABV. So by default, the results will be ordered by ABV highest to lowest. Both ABV and IBU are sortable, so you can order results by either of these fields using `sortby` in the query.
- The csv files are available on the openbeerdb.com site, but a small change the [beers.csv](../master/beerloader/data/beers.csv) file because it was malformed.  Hence they are part of this repo.
