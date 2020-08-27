# BF.ADD

Adds an item to the Bloom Filter, creating the filter if it does not yet exist.

```
>> BF.ADD bloom redis
(integer) 1
```




The above command returns "1" if the item was newly inserted, or "0" if it may have existed previously.

## BF.EXISTS

Determines whether an item may exist in the Bloom Filter or not.

Format: BF.EXISTS {key} {item}

```
>> BF.EXISTS bloom redis
(integer) 1
```

```
>> BF.EXISTS bloom rediss
(integer) 0
```

# BF.INSERT

This command will add one or more items to the bloom filter, by default creating it if it does not yet exist. 
There are several arguments which may be used to modify this behavior.

Format: BF.INSERT {key} [CAPACITY {cap}] [ERROR {error}] [EXPANSION expansion] [NOCREATE]
[NONSCALING] ITEMS {item...}

## Add three items to a filter, using default parameters if the filter does not already exist:


```
BF.INSERT filter ITEMS foo bar baz
```

In the above example, 
- "filter"  is the name of the filter, 
- ITEMS indicates the beginning of the items to be added to the filter. This parameter must be specified.


## Add one item to a filter, specifying a capacity of 10000 to be used if it does not already exist:

```
BF.INSERT filter CAPACITY 10000 ITEMS hello
```

In the above example, CAPCITY refers to the desired capacity for the filter to be created. 


## Add 2 items to a filter, returning an error if the filter does not already exist

```
BF.INSERT filter NOCREATE ITEMS foo bar
```

In the above example, NOCREATE  indicates that the filter should not be created if it does not already exist. Please note that NOCREATE can't be used either with CAPACITY or ERROR .

The above commands returns an array of booleans (integers). Each element is either true or false depending on whether the corresponding input element was newly
added to the filter or may have previously existed.



# BF.INFO 

Return information about key

Format  : BF.INFO {key}


Parameters 

key Name of the key to restore

```
 BF.INFO bloom
 1) Capacity
 2) (integer) 100
 3) Size
 4) (integer) 290
 5) Number of filters
 6) (integer) 1
 7) Number of items inserted
 8) (integer) 2
 9) Expansion rate
10) (integer) 2
```

# BF.MADD

Adds one or more items to the Bloom Filter, creating the filter if it does not yet exist. This command operates identically to BF.ADD except it allows multiple inputs and returns multiple values.

Format: BF.MADD {key} {item} [item...]

```
127.0.0.1:12543> BF.MADD bloom elem1 elem2 elem3
 1) (integer) 1
 2) (integer) 1
 3) (integer) 1
 ```
 
You can use BF.MEXISTS to retrieve return an array of booleans (integers). Each element is either true or false depending on whether the corresponding input element was newly added to the filter or may have previously existed.

 ```
 127.0.0.1:12543> BF.MEXISTS bloom elem1 elem2 elem3
 1) (integer) 1
 2) (integer) 1
 3) (integer) 1
 ```
