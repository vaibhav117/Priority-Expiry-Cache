# Take Home Submission
## Priority Expiry Cache
## Vaibhav Mathur

# Data Structures Used
1. **priority_hash**: This is a hashtable with priorities as keys. The values are Orderdicts having keys as indexes and values. The primary motive of these OrderedDicts is to preserve the order of usage of each key per each distinct priority number and allow O(1) access time if the Priority and Key are known. The format looks like - ```{ priority:{key:key} }```
   ```
   { 15:{'2':'2' , '5':'5'} , 1:{'1':'1','7':'7'} }
   ```
2. **expiry_hash**: This is a hashtable with expiry times as keys. The values are Simple Dicts having keys as indexes and values. The primary motive of these Dicts is to give O(1) access time if the Expiration Time and Key are known. The format looks like - ```{ expiry:{key:key} }```
    ```
   { 100:{'2':'2' , '5':'5'} , 3:{'1':'1','7':'7'} }
   ```
3. **hash_map**: This is the primary hashmap that stores the keys with their corresponding value, expiry and priority. The format looks like - ```{ key:{'expiry':expiry, 'value':value , 'priority':priority} }```
    ```
   { 'A':{'expiry': 100, 'value':1 , 'priority':5} } , 'B':{'expiry':3, 'value':2 , 'priority':5} } }
   ```
4. **expiry_present**: 
5. **priority_present**
6. **expiry_heap**
7. **priority_heap**

# Approach
The 
