
############################################### Vaibhav Mathur - Priority Expiry Cache #######################################################

from collections import deque
from collections import OrderedDict
import heapq
import time

class PriorityExpiryCache:
    def __init__(self, max_items, disable_expired_keys=False):
        assert (max_items>0)                        # Some corner cases fail if the size of the cache is 0
        self.global_start_time = time.time()
        self.max_items = max_items
        self.element_count = 0
        self.disable_expired_keys = disable_expired_keys

        self.priority_hash = {}                     # Hashmap of ordered dicts referenced against priority {priority:{key1:key1,key2:key2}}
        self.expiry_hash = {}                       # Hashmap of dicts referenced against expiry {expiry:{key1:key1,key2:key2}}
        self.hash_map = {}                          # Hashmap of individual elements, the value is a dict itself {key:{value:value,expiry:expiry,priority:priority}}
        
        #----------- Data Structures to maintain Heap Consistency
        self.expiry_present = {}                    # Hashmap to maintain list of expiry node in Heap (to track lazy operation)
        self.priority_present = {}                  # Hashmap to maintain list of priority node in Heap (to track lazy operation)
        self.expiry_heap = []                       # Heap to track Unique Expiries
        self.priority_heap = []                     # Heap to track Uinque Priorities
        
    def get_curr_time(self):
        return time.time() - self.global_start_time
    
    def Get(self, key):
        if key in self.hash_map:
            value = self.hash_map[key]["value"]
            priority = self.hash_map[key]["priority"]
            expiry = self.hash_map[key]["expiry"]
            #----------- Reinserting element in Ordered Dict
            self.priority_hash[priority].pop(key)
            self.priority_hash[priority][key] = key
            
            #-----------
            if disable_expired_keys and expiry < self.get_curr_time():
                return None
            else:
                return value
        else:
            return None
    
    def Set(self, key, value, priority, expiry):
        if key not in self.hash_map:
            if(self.element_count==self.max_items):                                         # Evicting Items if the cache is full
                self.evict_items()
            self.hash_map[key] = {'value':value , 'expiry':expiry , 'priority':priority}    # Adding element to main hashmap
            
            #----------- Adding element to expiry hash
            if expiry in self.expiry_hash:
                self.expiry_hash[expiry][key] = key
            else:
                self.expiry_hash[expiry] = {key:key}                                        # Is not required to be an Ordered Dict

            #----------- Adding element to priority hash
            if priority in self.priority_hash:
                self.priority_hash[priority][key] = key
            else:
                self.priority_hash[priority] = OrderedDict({key:key})
            
            #----------- Adding to Heap only if the element does not previously exist (could be because of lazy removal or non-unique val)
            if expiry not in self.expiry_present:
                heapq.heappush(self.expiry_heap , expiry)
                self.expiry_present[expiry] = 1

            #----------- Adding to Heap only if the element does not previously exist (could be because of lazy removal or non-unique val)
            if priority not in self.priority_present:
                heapq.heappush(self.priority_heap , priority)
                self.priority_present[priority] = 1
            
            self.element_count += 1

        else:
            old_val = self.hash_map[key]['value']
            old_expiry = self.hash_map[key]['expiry']
            old_priority = self.hash_map[key]['priority']

            #----------- Remove old values
            self.expiry_hash[old_expiry].pop(key)
            self.priority_hash[old_priority].pop(key)
            

            #----------- Add new values
            self.hash_map[key]['value'] = value
            self.hash_map[key]['expiry'] = expiry
            self.hash_map[key]['priority'] = priority

            self.expiry_hash[expiry][key] = key
            self.priority_hash[priority][key] = key
    
    def SetMaxItems(self, max_items):
        self.max_items = max_items
        while self.max_items < self.element_count:
            self.evict_items()

    def evict_items(self):
        #----------- Check for lazy eviction time values in the expiry_hash
        while( len(self.expiry_heap)>0 and len(self.expiry_hash[self.expiry_heap[0]]) == 0 ):
            self.expiry_present.pop(self.expiry_heap[0])           # Remove element from Hash Table tracking elements in Expiry Heap
            heapq.heappop(self.expiry_heap)                        # Remove element from the Actual Expiry Heap

        #----------- Check for lazy priority values in the priority_hash
        while( len(self.priority_heap)>0 and len(self.priority_hash[self.priority_heap[0]]) == 0 ):
            self.priority_present.pop(self.priority_heap[0])       # Remove element from Hash Table tracking elements in Priority Heap
            heapq.heappop(self.priority_heap)                      # Remove element from the Actual Priority Heap
            
        #----------- Check if there are elements to be evicted
        if self.element_count == 0:
            print("No Elements present in the cache!")
            return
        
        self.element_count -= 1

        #----------- After removing Expiry times which are not present, check for an expired item
        smallest_time = self.expiry_heap[0]
        if smallest_time < self.get_curr_time():
            key_to_be_evicted , _ = list(self.expiry_hash[smallest_time].items())[0]                   # Simply Picking the first element from the dict having the specific expiry time
            priority_of_key_to_be_evicted = self.hash_map[key_to_be_evicted]['priority']
            self.expiry_hash[smallest_time].pop(key_to_be_evicted)                                     # Removing element from expiry hashmap
            self.priority_hash[priority_of_key_to_be_evicted].pop(key_to_be_evicted)                    # Removing element from priority hashmap
            self.hash_map.pop(key_to_be_evicted)                                                        # Removing element from get hashmap

        #----------- If no Expired items exist, removing element of lowest priority which is the Least Recently Used for that particular priority
        else:
            priority_of_key_to_be_evicted = self.priority_heap[0]                                       # Getting the lowest Priority Value from the Priority Heap
            key_to_be_evicted , _ = list(self.priority_hash[priority_of_key_to_be_evicted].items())[0]  # Getting the first(oldest) element from the Ordered Dict for the lowest priority value
            expiry_of_key_to_evicted = self.hash_map[key_to_be_evicted]['expiry']                       # Getting the expiry of the selected element
            self.expiry_hash[expiry_of_key_to_evicted].pop(key_to_be_evicted)                          # Removing element from expiry hashmap
            self.priority_hash[priority_of_key_to_be_evicted].pop(key_to_be_evicted)                    # Removing element from priority hashmap
            self.hash_map.pop(key_to_be_evicted)                                                        # Removing element from get hashmap
        

class TestCase:
    def __init__(self, max_items, disable_expired_keys=False):
        if max_items<=0:
            print("Please test for Cahce size greater than 1")
        self.pec = PriorityExpiryCache(max_items, disable_expired_keys=disable_expired_keys)
    
    def Get(self, key):
        val = self.pec.Get(key=key)
        if val == None:
            print(f"{key} not present in the Cache")
        else:
            print(f"Value for {key}: {val}")
    
    def Set(self, key, value, priority, expiry):
        self.pec.Set(key=key, value=value, priority=priority, expiry=expiry)

    def SetMaxItems(self, max_items):
        self.pec.SetMaxItems(max_items=max_items)

    def GetAllKeys(self):                                               # Please note that the keys returned are not in the order of last usage
        keys = []                                                       # These are just keys that have not yet been evicted (can have expired keys)
        for key, value in self.pec.hash_map.items():
            keys.append(key)
        return keys

def run_test1(disable_expired_keys):
    print(f"\n----------- Running Test-1 ---------------")
    max_items = 5
    test1 = TestCase(max_items=max_items, disable_expired_keys=False)
    test1.Set("A", value=1, priority=5,  expiry=100)
    test1.Set("B", value=2, priority=5, expiry=3)
    test1.Set("C", value=3, priority=5,  expiry=10)
    test1.Set("A", value=10, priority=5,  expiry=100)
    test1.Get("A")
    test1.Get("B")
    test1.Set("D", value=4, priority=5,  expiry=100)
    test1.Set("E", value=5, priority=5,  expiry=100)
    test1.Set("F", value=6, priority=5,  expiry=100)
    test1.Get("C")
    test1.Get("B")
    time.sleep(5)
    test1.Set("G", value=7, priority=5,  expiry=100)
    test1.Get("B")

def run_test2(disable_expired_keys):
    print(f"\n----------- Running Test-2 ---------------")
    max_items = 5
    test2 = TestCase(max_items=max_items, disable_expired_keys=False)
    test2.Set("A", value=1, priority=5,  expiry=100)
    test2.Set("B", value=2, priority=15, expiry=3)
    test2.Set("C", value=3, priority=5,  expiry=10)
    test2.Set("D", value=4, priority=1,  expiry=15)
    test2.Set("E", value=5, priority=5,  expiry=150)
    time.sleep(5)
    test2.SetMaxItems(max_items=4)
    print(test2.GetAllKeys())
    test2.SetMaxItems(max_items=3)
    print(test2.GetAllKeys())
    test2.SetMaxItems(max_items=2)
    print(test2.GetAllKeys())
    test2.SetMaxItems(max_items=1)
    print(test2.GetAllKeys())

if __name__ == "__main__":
    disable_expired_keys = False
    run_test1(disable_expired_keys)
    run_test2(disable_expired_keys)