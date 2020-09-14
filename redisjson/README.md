# Redis JSON Datasets

RedisJSON provides in-memory manipulation of JSON documents at high velocity and volume. With RedisJSON, you can natively store document data in a hierarchical, tree-like format to scale and query documents efficiently, significantly improving performance over storing and manipulating JSON with Lua and core Redis data structures.

In the next steps you will use some basic RedisJSON commands, you can run them from the redis-cli or using the CLI available in RedisInsight. (Click on “CLI” in the RedisInsight left menu).

To interact with RedisJSON you will most of the time use the JSON.SET and JSON.GET command. Before using RedisJSON, you should familiarize yourself with its commands and syntax as detailed in the commands reference document.
Let’s go ahead and test drive the below JSON specific operations:

- Setting/Retrieving a Redis Key with a JSON value
- Scalar
- Objects(including Nested Objects)
- Arrays of JSON Objects
- JSON Nested Objects

## Setting a Redis Key with JSON value

### 1.1 Scalar

Use JSON.SET to set the JSON value at path in key. For new Redis keys the path must be the root. For existing keys, when the entire path exists, the value that it contains is replaced with the json value.

```
>> JSON.SET scalar .  ' "Hello JSON!" '
"OK"
```

Use JSON.GET to return the value at path in JSON serialized form

```
>> JSON.GET scalar
"\"Hello JSON!\""
```

### 1.2  Objects

Let us look at JSON Object Example. A JSON object contains data in the form of a key/value pair. The keys are strings and the values are the JSON types. Keys and values are separated by colon. Each entry (key/value pair) is separated by comma.

The { (curly brace) represents the JSON object.

```
{  
    "employee": {  
        "name": "alpha",   
        "age": 40,   
        "married": true  
    }  
}  
```

Below is the command to insert JSON data into Redis:

```
>> JSON.SET employee_profile . '{ "employee": { "name": "alpha", "age": 40,"married": true }  } '
"OK"
```

The following subcommands below changes the reply's format and are all set to the empty string by default: * INDENT sets the indentation string for nested levels * NEWLINE sets the string that's printed at the end of each line * SPACE sets the string that's put between a key and a value

```
>> >> JSON.GET employee_profile
"{\"employee\":{\"name\":\"alpha\",\"age\":40,\"married\":true}}"
```

### 1.2.1 Retrieving a part of JSON document

If we want to retrieve a part of the JSON document from Redis, it is still possible. In the below example, “.ans” can be passed in the commandline to retrieve the value 4.

```
>> JSON.SET object . '{"foo":"bar", "ans":"4" }'
"OK"
```

```
>> JSON.GET object
"{\"foo\":\"bar\",\"ans\":\"4\"}"
```

```
>> JSON.GET object .ans
"\"4\""
```

### 1.2.2 Retrieving the type of JSON data

JSON.TYPE  reports the type of JSON value at path and path defaults to root if not provided. If the key or path do not exist, null is returned.

```
>> JSON.TYPE employee_profile
"Object"
```

### 1.3 JSON Arrays of Objects

The JSON array represents an ordered list of values. JSON array can store multiple values. It can store string, number, boolean or object in JSON array.
In JSON arrays, values must be separated by comma. The [ (square bracket) represents JSON array.

Let's see a simple JSON array example having 4 objects.
 
```
{"employees":[    
    {"name":"Alpha", "email":"alpha@gmail.com", "age":23},    
    {"name":"Beta", "email":"beta@gmail.com", "age":28},  
    {"name":"Gamma", "email":"gamma@gmail.com", "age":33},    
    {"name":"Theta", "email":"theta@gmail.com", "age":41}   
]}  
```

```
>> JSON.SET testarray . '  {"employees":[ {"name":"Alpha", "email":"alpha@gmail.com", "age":23}, {"name":"Beta", "email":"beta@gmail.com", "age":28},  {"name":"Gamma", "email":"gamma@gmail.com", "age":33}, {"name":”Theta", "email":"theta@gmail.com", "age":41}  ]}  '
"OK"
```

```
>> JSON.GET testarray
"{\"employees\":[{\"name\":\"Alpha\",\"email\":\alpha@gmail.com\",\"age\":23},{\"name\":\"Beta\",\"email\":\"beta@gmail.com....
```

### 1.3.1 JSON Nested Object Example

It is possible that a JSON object can have another object too. Let's see a simple example of a JSON object having another object.

```
>> JSON.SET employee_info . ' { "firstName": "Alpha",         "lastName": "K", "age": 23,        "address" : {            "streetAddress": "110 Fulbourn Road Cambridge",  "city": "San Francisco", "state": "California", "postalCode": "94016"  } } '
"OK"
```

```
>> JSON.GET employee_info
"{\"firstName\":\"Alpha\",\"lastName\":\"K\",\"age\":23,\"address\":{\"streetAddress\":\"110 Fulbourn Road Cambridge\",\"city\":\"San Francisco\",\"state\":\"California\",\"postalCode\":\"94016\"}}"
```

## Landslide Dataset 

Reference: https://data.gov.ie/dataset/gsi-landslide-events-data
