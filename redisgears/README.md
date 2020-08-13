# IMDB Sample Data for RedisGears

Sample IMDB dataset for RedisGears

## How to execute this example

### Set up you redis server with RedisGears

### Download the IMDB data from the below link and extract it to the current directory:

https://datasets.imdbws.com/title.basics.tsv.gz

#### Execute the below python script

```python UploadImdb.py```

#### Run th below RedisGraph command

```RG.PYEXECUTE "GB('KeysOnlyReader').map(lambda x: execute('hget', x, 'genres')).flatmap(lambda x: x.split(',')).countby().run()"```
