# Redis JSON Datasets



Syntax:

```
JSON.SET <key> <path> <json>
```

It sets the JSON value at path in key. For new Redis keys the path must be the root. For existing keys, when the entire path exists, the value that it contains is replaced with the json value.

## How to insert JSON data into Redis


Consider 

{  
    "employee": {  
        "name":       "alpha",   
        "age":      40,   
        "married":    true  
    }  
}  

```
>> JSON.SET employee_profile   .   '{       "employee": {           "name":       "alpha",     "age":      40,    "married":    true   }   } '
"OK"
```

```
>> >> JSON.GET employee_profile
"{\"employee\":{\"name\":\"alpha\",\"age\":40,\"married\":true}}"
```

