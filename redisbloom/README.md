# Redis Bloom Datasets

- RedisBloom provides Redis with support for additional probabilistic data structures. 
- These structures allow for constant memory space and extremely fast processing while still maintaining a low error rate. 
- RedisBloom module provides four data types which are briefed below:

  - Bloom filter:  It is a probabilistic  data structure that can test for presence. A data structure designed to rapidly determine if an element is present in a set in a highly memory-efficient manner. 
  - Cuckoo filter: An alternative to Bloom filters with additional support for deletion of elements from a set.
  - Count-Min Sketch: Calculates frequency of events in data samples.
  - Top-K: A deterministic algorithm that approximates frequencies for the top k items.


To interact with RedisBloom, you will most of the time use the BF.ADD and BF.EXISTS command. 

You will create a very basic dataset based on unique visitor’s IP address, and you will see how to:

- Create a bloom filter
- Determine whether an item exist in the Bloom Filter or not
- Add one or more items to the bloom filter
- Determining if unique visitor’s IP address exists or not
- Debug bloom filters


## Create a Bloom filter

Use  BF.ADD to add a unique visitor IP address to the Bloom Filter as shown below:

```
>> BF.ADD unique_visitors 10.94.214.120
(integer) 1
(1.75s)
```

## Determine whether the unique visitor’s IP address exists or not

Use BF.EXISTS  to determine whether an item may exist in the Bloom Filter or not.

```
>> BF.EXISTS unique_visitors 10.94.214.120
(integer) 1
```

```
>> BF.EXISTS unique_visitors 10.94.214.121
(integer) 0
(1.46s)
```

## Add one or more items to the bloom filter

Use BF.MADD to add one or more items to the Bloom Filter, creating the filter if it does not yet exist. This command operates identically to BF.ADD except it allows multiple inputs and returns multiple values.

```
>> BF.MADD unique_visitors 10.94.214.100 10.94.214.200 10.94.214.210 10.94.214.212
1) (integer) 1
2) (integer) 1
3) (integer) 1
4) (integer) 1
```

## Determining if unique visitor’s IP address exists or not

Use BF.MEXISTS to determine if one or more items may exist in the filter or not.

```
>> BF.MEXISTS unique_visitors 10.94.214.200 10.94.214.212
1) (integer) 1
2) (integer) 1
```

```
>> BF.MEXISTS unique_visitors 10.94.214.200 10.94.214.213
1) (integer) 1
2) (integer) 0
```

## Debugging Bloom Filters

Use BF.DEBUG to see exactly how the filter is being utilized. This outputs the total number of elements as the first result, and then a list of details for each filter in the chain. As you can see, whenever a new filter is added, its capacity grows exponentially and the strictness for errors increases.

```
>> BF.DEBUG unique_visitors
1) "size:8"
2) "bytes:138 bits:1104 hashes:8 hashwidth:64 capacity:100 size:8 ratio:0.005"
```
