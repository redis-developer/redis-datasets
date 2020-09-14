# A Curated List of Redisgraph datasets

- [Redis Movie Database](https://github.com/Redis-Developer/redis-datasets/blob/master/redisgraph/datasets/redis-movie-database/README.md)
- [An API of Ice and Fire](https://anapioficeandfire.com/)


# Redisgraph Bulk Loader Tools

- [Redis Graph Bulk Loader Script](https://github.com/Redis-Developer/redis-datasets/tree/master/redisgraph/redisgraph-bulk-loader)

# Redisgraph & Redisearch together

-  [Demonstration of using RedisGraph and RediSearch together](https://github.com/stockholmux/conf19-search-graph-demo)

## Getting Started with RedisGraph

RedisGraph is a Redis module that enables enterprises to process any kind of connected data faster than traditional relational or existing graph databases. It implements a unique data storage and processing solution (with sparse adjacency matrices and GraphBLAS) to deliver the fastest and most efficient way to store, manage and process connected data in graphs. With RedisGraph, we can process complex transactions 10 - 600 times faster than traditional graph solutions and require 50-60% fewer memory resources than any other graph database in the market!

### Getting started

To leverage the RedisGraph module, you will have to create a new Redis Cloud Essential Database with the RedisGraph module enabled as shown below.




In the next steps you will use some basic RediGraph commands, you can run them from the redis-cli or using the CLI available in RedisInsight. (Click on “CLI” in the RedisInsight left menu).

To interact with RedisGraph you will most of the time use the GRAPH.QUERY command and execute Cypher queries,

### 1 - Insert Data into a Graph

### 1.1 Insert Actors

Let’s start to insert some actors into the graph:movies graph, that will be automatically created during this command.

```
>> GRAPH.QUERY graph:movies "CREATE (:Actor {name:'Mark Hamill', actor_id:1}), (:Actor {name:'Harrison Ford', actor_id:2}), (:Actor {name:'Carrie Fisher', actor_id:3})"

1) 1) "Labels added: 1"
   2) "Nodes created: 3"
   3) "Properties set: 6"
   4) "Query internal execution time: 0.675400 milliseconds"
Using this single query you have created three actors with their name and an id.
```

### 1.2 Insert a Movie

```
> GRAPH.QUERY graph:movies "CREATE (:Movie {title:'Star Wars: Episode V - The Empire Strikes Back', release_year: 1980 , movie_id:1})"
1) 1) "Labels added: 1"
   2) "Nodes created: 1"
   3) "Properties set: 3"
   4) "Query internal execution time: 0.392300 milliseconds"
```

Using this single query you have created a movie with a title, the release year and an id.

### 1.3 Associate actors and movie

The core of a graph is the relationships between the nodes allowing the applications to navigate and query them. Let’s create a relationship between the actors and the movie.

```
> GRAPH.QUERY graph:movies "MATCH (a:Actor),(m:Movie) WHERE a.actor_id = 1 AND m.movie_id = 1 CREATE (a)-[r:Acted_in {role:'Luke Skywalker'}]->(m) RETURN r"
1) 1) "r"
2) 1) 1) 1) 1) "id"
            2) (integer) 1
         2) 1) "type"
            2) "Acted_in"
         3) 1) "src_node"
            2) (integer) 0
         4) 1) "dest_node"
            2) (integer) 3
         5) 1) "properties"
            2) 1) 1) "role"
                  2) "Luke Skywalker"
3) 1) "Properties set: 1"
   2) "Relationships created: 1"
   3) "Query internal execution time: 0.664800 milliseconds"
```

Created a new relation between the actor Mark Hamill indicating that he acted in Star Wars: Episode V  as Luke Skywalker.

Let’s repeat this for the other actors:

```
> GRAPH.QUERY graph:movies "MATCH (a:Actor), (m:Movie) WHERE a.actor_id = 2 AND m.movie_id = 1 CREATE (a)-[r:Acted_in {role:'Han Solo'}]->(m) RETURN r"
> GRAPH.QUERY graph:movies "MATCH (a:Actor), (m:Movie) WHERE a.actor_id = 3 AND m.movie_id = 1 CREATE (a)-[r:Acted_in {role:'Princess Leila'}]->(m) RETURN r"
```

It is also possible to create everything in a single query for example:

```
> GRAPH.QUERY graph:movies "CREATE (:Actor {name:'Marlo Brando', actor_id:4})-[:Acted_in {role:'Don Vito Corleone'}]->(:Movie {title:'The Godfather', release_year: 1972 , movie_id:2})"

1) 1) "Nodes created: 2"
   2) "Properties set: 6"
   3) "Relationships created: 1"
   4) "Query internal execution time: 0.848500 milliseconds"
```

### 1 - Querying the Graph

Now that you have data in your graph it is time to ask questions such as:

### “What is the title of all movies?”

```
> GRAPH.QUERY graph:movies "MATCH (m:Movie) RETURN m.title"

1) 1) "m.title"
2) 1) 1) "Star Wars: Episode V - The Empire Strikes Back"
   2) 1) "The Godfather"
3) 1) "Query internal execution time: 0.349400 milliseconds"
```

### “What is the information of the movie with the id equals 1?”

```
> GRAPH.QUERY graph:movies "MATCH (m:Movie) WHERE m.movie_id = 1 RETURN m"

1) 1) "m"
2) 1) 1) 1) 1) "id"
            2) (integer) 3
         2) 1) "labels"
            2) 1) "Movie"
         3) 1) "properties"
            2) 1) 1) "title"
                  2) "Star Wars: Episode V - The Empire Strikes Back"
               2) 1) "release_year"
                  2) (integer) 1980
               3) 1) "movie_id"
                  2) (integer) 1
3) 1) "Query internal execution time: 0.365800 milliseconds"
```

### “Who are the actors of the'Star Wars: Episode V - The Empire Strikes Back' movie and their role?”

```
> GRAPH.QUERY graph:movies "MATCH (a:Actor)-[r:Acted_in]-(m:Movie) WHERE m.movie_id = 1 RETURN a.name,m.title,r.role"
1) 1) "a.name"
   2) "m.title"
   3) "r.role"
2) 1) 1) "Mark Hamill"
      2) "Star Wars: Episode V - The Empire Strikes Back"
      3) "Luke Skywalker"
   2) 1) "Harrison Ford"
      2) "Star Wars: Episode V - The Empire Strikes Back"
      3) "Han Solo"
   3) 1) "Carrie Fisher"
      2) "Star Wars: Episode V - The Empire Strikes Back"
      3) "Princess Leila"
3) 1) "Query internal execution time: 0.641200 milliseconds"
```

Take a look at the Cypher language to learn more about all the capabilities.


