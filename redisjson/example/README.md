# Redis JSON Datasets



Syntax:

```
JSON.SET <key> <path> <json>
```

It sets the JSON value at path in key. For new Redis keys the path must be the root. For existing keys, when the entire path exists, the value that it contains is replaced with the json value.

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

```
>> >> JSON.GET employee_profile
"{\"employee\":{\"name\":\"alpha\",\"age\":40,\"married\":true}}"
```

