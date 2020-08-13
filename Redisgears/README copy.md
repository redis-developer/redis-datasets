# ImdbExample
RedisGears Imdb Example

## Run the Example
* Set up you redis server with RedisGears
* Download the IMDB data from this link and extract it to the current directory: https://datasets.imdbws.com/title.basics.tsv.gz
* run `python UploadImdb.py`
* run `RG.PYEXECUTE "GB('KeysOnlyReader').map(lambda x: execute('hget', x, 'genres')).flatmap(lambda x: x.split(',')).countby().run()"`
