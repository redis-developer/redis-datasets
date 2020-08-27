# BF.ADD

Adds an item to the Bloom Filter, creating the filter if it does not yet exist.

```
redis-17937.c212.ap-south-1-1.ec2.cloud.redislabs.com:17937> BF.ADD bloom redis
(integer) 1
```




The above command returns "1" if the item was newly inserted, or "0" if it may have existed previously.

## BF.EXISTS

Determines whether an item may exist in the Bloom Filter or not.

Format: BF.EXISTS {key} {item}

```
redis-17937.c212.ap-south-1-1.ec2.cloud.redislabs.com:17937> BF.EXISTS bloom redis
(integer) 1
```

```
redis-17937.c212.ap-south-1-1.ec2.cloud.redislabs.com:17937> BF.EXISTS bloom rediss
(integer) 0
```

# BF.INSERT

This command will add one or more items to the bloom filter, by default creating it if it does not yet exist. 
There are several arguments which may be used to modify this behavior.

## Add three items to a filter, using default parameters if the filter does not already exist:


```
BF.INSERT filter ITEMS foo bar baz
```

## Add one item to a filter, specifying a capacity of 10000 to be used if it does not already exist:

```
BF.INSERT filter CAPACITY 10000 ITEMS hello
```

## Add 2 items to a filter, returning an error if the filter does not already exist

```
BF.INSERT filter NOCREATE ITEMS foo bar
```

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

