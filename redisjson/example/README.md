# Redis JSON Datasets

- Keys can contain any valid JSON values
  - scalars, objects or arrays
  - Nested or not
- Data is stored decoded in binary format
- JSONPath like syntax for direct access to elements
- Strongly typed atomic commands


## Scalar

Syntax:

```
JSON.SET <key> <path> <json>
```

It sets the JSON value at path in key. For new Redis keys the path must be the root. For existing keys, when the entire path exists, the value that it contains is replaced with the json value.


```
>> JSON.SET scalar .  ' "Hello JSON!" '
"OK"
```
```
>> JSON.GET scalar
"\"Hello JSON!\""
```


## Objects

```
>> JSON.SET object . '{"foo":"bar", "ans":"4" }'
"OK"
>> JSON.GET object
"{\"foo\":\"bar\",\"ans\":\"4\"}"
```
```
>> JSON.GET object .ans
"\"4\""
```



## How to insert JSON data into Redis

Let us look at JSON Object Example. A JSON object contains data in the form of key/value pair. The keys are strings and the values are the JSON types. Keys and values are separated by colon. Each entry (key/value pair) is separated by comma.

The { (curly brace) represents the JSON object.

```
{  
    "employee": {  
        "name":       "alpha",   
        "age":      40,   
        "married":    true  
    }  
}  
```

```
>> JSON.SET employee_profile   .   '{       "employee": {           "name":       "alpha",     "age":      40,    "married":    true   }   } '
"OK"
```



## JSON.GET

### Syntax

```
JSON.GET <key>
         [INDENT indentation-string]
         [NEWLINE line-break-string]
         [SPACE space-string]
         [NOESCAPE]
         [path ...]
```

It return the value at path in JSON serialized form.This command accepts multiple path s, and defaults to the value's root when none are given.

The following subcommands change the reply's format and are all set to the empty string by default: * INDENT sets the indentation string for nested levels * NEWLINE sets the string that's printed at the end of each line * SPACE sets the string that's put between a key and a value

```
>> >> JSON.GET employee_profile
"{\"employee\":{\"name\":\"alpha\",\"age\":40,\"married\":true}}"
```

## JSON.TYPE

### Syntax 

JSON.TYPE <key> [path]

It reports the type of JSON value at path and path defaults to root if not provided. If the key or path do not exist, null is returned.

```
>> JSON.TYPE employee_profile
"object"
```


## 
