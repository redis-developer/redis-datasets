# Redis Movie Database Sample Dataset

This dataset contains, movies and actors stored as Redis Hash.

This dataset could be used for:
* Redis Core
* RediSearch
* RedisGraph


### Movies

The movie hashes contain the following fields: 

* **`movie:id`** : The key of the hash.
* **`title`** : The title of the movie.
* **`plot`** : A summary of the movie.
* **`genre`** : The genre of the movie, for now a movie will only h ave one single genre.
* **`release_year`** : The year the movie has been released as a numerical value.
* **`rating`** : The ratings from the public numerical value.
* **`votes`** : Number of votes.
* **`poster`** : Link to the movie poster.
* **`imdb_id`** : id of the movie in the [IMDB](https://imdb.com) database.


<details> 
  <summary>Sample Data: <b>movie:343</b></summary>
  <table>
      <thead>
        <tr>
            <th>Field</th>
            <th>Value</th>
        </tr>
    </thead>
  <tbody>
    <tr>
        <th>title</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        Spider-Man
        </td>
    </tr>
    <tr>
        <th>plot</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        When bitten by a genetically modified spider a nerdy shy and awkward high school student gains spider-like abilities that he eventually must use to fight evil as a superhero after tragedy befalls his family.
        </td>
    </tr>
    <tr>
        <th>genre</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        Action
        </td>
    </tr>
    <tr>
        <th>release_year</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        2002
        </td>
    </tr>
    <tr>
        <th>rating</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        7.3
        </td>
    </tr>
    <tr>
        <th>votes</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        662219
        </td>
    </tr>
    <tr>
        <th>poster</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        https://m.media-amazon.com/images/M/MV5BZDEyN2NhMjgtMjdhNi00MmNlLWE5YTgtZGE4MzNjMTRlMGEwXkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_SX300.jpg
        </td>
    </tr>
    <tr>
        <th>imdb_id</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        tt0145487
        </td>
    </tr>
    <tbody>
  </table>
</details>


### Actors

The actor hashes contain the fields described earlier.

* **`actor:id`** : The key of the hash.
* **`first_name`** : First Name.
* **`last_name`** : Last Name.
* **`date_of_birth`** : Year of birth.



<details> 
  <summary>Sample Data: <b>actor:64</b></summary>
  <table>
      <thead>
        <tr>
            <th>Field</th>
            <th>Value</th>
        </tr>
    </thead>
  <tbody>
    <tr>
        <th>first_name</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        Denzel
        </td>
    </tr>

    <tr>
        <th>first_name</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        Washington
        </td>
    </tr>

    <tr>
        <th>date_of_birth</th>
        <td style='font-family:monospace; font-size: 0.875em; "'>
        1954
        </td>
    </tr>

    <tbody>
  </table>
</details>


## Importing the dataset

The dataset files are  `redis-cli` scripts that you can import using the following command:


```
> redis-cli -h localhost -p 6379 < ./import_movies.redis


> redis-cli -h localhost -p 6379 < ./import_actors.redis

```

Once done you can check some data:

```
> HMGET "movie:343" title release_year genre

1) "Spider-Man"
2) "2002"
3) "Action"
```

```
> HGETALL "actor:64"

1) "first_name"
2) "Denzel"
3) "last_name"
4) "Washington"
5) "date_of_birth"
6) "1954"
```


You can now use this dataset in your applications.

