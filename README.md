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
4. **expiry_present**: This is a hashmap that tracks all the priorities that at that instant exist in the priority_heap. The format looks like - ```{ expiry:1 }```
    ```
   { 100:1 , 3:1 }
   ```
5. **priority_present**: This is a hashmap that tracks all the expiry times that at that instant exist in the priority_heap. The format looks like - ```{ priority:1 }```
    ```
   { 5:1 }
   ```
6. **expiry_heap**: This is a min heap of all the expiry times. It is used to get the min expiry time. There are no repetitions of values in the heap. The values removal from this expiry heap is done in a lazy manner. It might also have expiry times for which there are no elements. Therefore, before picking the lowest time, we keep poping expiry values till we get a value for which there are elements. The heap elements just hold the expiry time.
   
7. **priority_heap**: This is a min heap of all Priorities. It's used to get the min priorities. There are no repititions of values in the heap. The values removal from this priority heap is done in a lazy manner. It might also have priorities for which there are no elements. Therefore, before picking the lowest priority, we keep poping priority values till we get a value for which there are elements. The heap elements just hold the priority.

# Approach
Instead of implementing a Heap using Linked List from scratch, I wanted to use Python's implementation of heap as it has many internal optamisations. But that posed a new issue of deleting elements from the heap when all elements of the corresponding Expiry Time or Priority were evicted from the Cache.
To get around this problem, I've adopted lazy deletion from Expiry and Priority heaps.
Essentially, I don't delete elements from the heaps immediately. They are cleared from the heap, when during the next ```evict_items()``` call, till a values of Expiry Time or Priority is found for which elements still exist. This process of removing stale values from the heaps and find the Expiry Time or Priority for the element to be evicted still takes ```log(e) + log(p)``` time.

# Function Discription
1. **Get(key)**: To get the value for a key, I do the following steps-
   - Check if the key exists in the hash_map dict.
   - If it does not, I simply return None.
   - If it does, I return the value and reinsert the element into Orderdict for its specific priority number in the Orderdicts hashmap. This takes care last used ordering of all elements having the same priority number.
   - Add the Priority and Expiry Time vlaues to the heaps if they don't already exist in them.
   - ```O(1)``` time complexity even in the worst case

2. **Set(key, value, priority, expiry)**
   - If the elements already exists, move element to the Orderdict for the new Priority Number and Expiry Number.
   - If the element does not exist, then call ```evict_item()``` if the Cache is full.
   - Insert the element, into hash_map, priority_hash and expiry_hash.
   - Add the Priority and Expiry Time values to the heaps if they don't already exist in them.
   - ```O(1)``` time complexity in the worst case.

3. **evict_item()**: It carries out evictions based on the 3 rules given.
   - Firstly, expiry_heap and priority_heap are repeatedly poped till Expiry Times and Priority values without any corresponding elements are at the top to carry out lazy deletions. This takes ```O(log e) + O(log p)``` time
   - Then, if an expired element exists, I delete it from priority_hash, expiry_hash and hash_map. This takes ```O(1)``` time.
   - In case of no expired items, we get lowest Priority Index and simply evict the least-recently-used element. This too takes ```O(1)``` time.
  
4. **SetMaxItems(max_items)**: Allows for altering the cache size.
   - It repeatedly calls ```evict_item()``` till the number of elements are not higher than the new max capacity.


# Time Complexities
1. Get: ```O(1)```
2. Set: ```O(1)```
3. evict_items: ```O(log e + log p)```


In my implementaiton, I only call ```evict_items()``` to abide by the size constrins.
Therefore, ```Get()``` can potentially yield expired values as well.
To check that, I have added a ```disable_expired_keys``` option. However, disable_expired_keys will only keep expired values from from being returned in the ```Get()``` call.