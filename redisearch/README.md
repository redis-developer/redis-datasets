
# RediSearch

RediSearch is a powerful text search and secondary indexing engine, built on top of Redis as a Redis module. It is extremely fast compared to other open-source search engines.
It is written in C. It implements multiple data types and commands that fundamentally change what you can do with Redis.

## Getting Started 

In the next steps you will use some basic RediSearch commands, you can run them from the redis-cli or using the CLI available in RedisInsight. (Click on “CLI” in the RedisInsight left menu).

You will create a very basic dataset based on movies informations, and you will see how to:

- Create an index
- Insert data
- Query data

### 1 - Create an Index

The first thing to do is to create an index with a schema. This index will be used to index data and do some advance search and aggregation queries.

```
> FT.CREATE idx:movies SCHEMA title TEXT SORTABLE release_year NUMERIC SORTABLE rating NUMERIC SORTABLE genre TAG SORTABLE
```

The command above:

- Create an index named idx:movies
- With a schema made of four fields:
  - title
  - release_year
  - rating
  - genre

If you want to learn more about all the options available when you create an index you can look at the FT.CREATE command documentation, you can update an index with the FT.ALTER command, and drop it using FT.DROP.


### 2 - Insert Movies

Use the command FT.ADD to add new movies to the index.

```
> FT.ADD  idx:movies movies:1002 1.0 FIELDS  title "Star Wars: Episode V - The Empire Strikes Back" plot "Luke Skywalker begins Jedi training with Yoda"  release_year 1980 genre "Action" rating 8.7 nb_of_votes 1127635 imdb_id tt0080684
```

```
> FT.ADD  idx:movies movies:1003 1.0 FIELDS title "The Godfather" plot "The aging patriarch transfers control of his clandestine to his son."  release_year 1972 genre "Drama" rating 9.2 nb_of_votes 1563839 imdb_id tt0068646
```

You have now two movies in your database, the FT.ADD command parameter are used as follow:

 - idx:movies : the name of the index to used
 - movies:1003 : the document id, will be used to create a hash, see FIELDS parameter.
 - 1.0 : the score used for this document, used to rank documents
 - FIELDS : the list of all the fields associated with the document. All the fields that have been defined in the index schema will be indexed.

As described above a hash is created you can see it using the following command:

```
>>  HGETALL movies:1003
 1) "nb_of_votes"
 2) "1563839"
 3) "title"
 4) "The Godfather"
 5) "rating"
 6) "9.2"
 7) "imdb_id"
 8) "tt0068646"
 9) "plot"
10) "The aging patriarch transfers control of his clandestine to his son."
11) "genre"
12) "Drama"
13) "release_year"
14) "1972"
```

If you want to learn more about all the options available when you create a new document look at the FT.ADD command documentation, and use FT.DEL to remove the document from the index.

### 3 - Search the Movies

You can now use the FT.SEARCH to search your database, for example:

#### Search all movies sorted by release year:

```
>  FT.SEARCH idx:movies * SORTBY release_year ASC RETURN 2 title release_year
1) (integer) 2
2) "movies:1003"
3) 	1) "release_year"
	2) "1972"
	3) "title"
	4) "The Godfather"
4) "movies:1002"
5) 	1) "release_year"
   	2) "1980"
   	3) "title"
	4) "Star Wars: Episode V - The Empire Strikes Back"
```

#### Search “action” movies that contains “star” in the index (with current index it will be only in the title)

```
>  FT.SEARCH idx:movies "star @genre:{action}" RETURN 2 title release_year
1) (integer) 1
2) "movies:1002"
3) 	1) "title"
	2) "Star Wars: Episode V - The Empire Strikes Back"
	3) "release_year"
	4) "1980"
```

The FT.SEARCH command is the base command to search your database, it has many options and is associated with a very powerful and rich query syntax that you can find in the documentation.

It is also possible to use the index to do data aggregation using FT.AGGREGATE command.



# Sample Datasets for Redisearch

## RediSearch and Regisgraph together

- [Demonstration of using RedisGraph and RediSearch together](https://github.com/stockholmux/conf19-search-graph-demo)
