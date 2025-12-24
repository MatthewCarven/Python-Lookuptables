import time
import random
import string
import collections

# --- 1. The "Naive" Standard List ---
class StandardList:
    def __init__(self):
        self.data = []
    
    def add_unique(self, word):
        # O(N) penalty: Must scan entire list to ensure uniqueness
        if word not in self.data:
            self.data.append(word)
            
    def find(self, word):
        # O(N) penalty: Must scan entire list to find the word
        return word in self.data

# --- 2. Your "Bucketed" Solution ---
class BucketedList:
    def __init__(self):
        # Creates 26 buckets: {'A': [], 'B': [], ...}
        self.buckets = collections.defaultdict(list)
    
    def add_unique(self, word):
        first_char = word[0].upper()
        # O(N/26) bonus: Only scan the small bucket 'A', not the whole list
        if word not in self.buckets[first_char]:
            self.buckets[first_char].append(word)
            
    def find(self, word):
        first_char = word[0].upper()
        # O(N/26) bonus: Only look inside the relevant bucket
        if first_char in self.buckets:
            return word in self.buckets[first_char]
        return False

# --- Setup Data ---
# Generate 10,000 random "words" to fill the DB first
print("Generating data...")
data_pool = [''.join(random.choices(string.ascii_uppercase, k=5)) for _ in range(10000)]
search_terms = [''.join(random.choices(string.ascii_uppercase, k=5)) for _ in range(10000)]

# Initialize both lists with the initial data
std_list = StandardList()
my_buckets = BucketedList()

for word in data_pool:
    std_list.add_unique(word)
    my_buckets.add_unique(word)

print(f"Database size: {len(std_list.data)} unique items.\n")

# --- TEST 1: INSERT BENCHMARK ---
# We will try to add 1,000 NEW items. 
# Each add requires a check to ensure it doesn't already exist.

new_items = [''.join(random.choices(string.ascii_uppercase, k=5)) for _ in range(10000)]

# Time Standard List
start = time.perf_counter()
for item in new_items:
    std_list.add_unique(item)
end = time.perf_counter()
std_time = end - start

# Time Bucketed List
start = time.perf_counter()
for item in new_items:
    my_buckets.add_unique(item)
end = time.perf_counter()
bucket_time = end - start

print(f"--- INSERT RESULTS (10000 items) ---")
print(f"Standard List:  {std_time:.6f} seconds")
print(f"Bucketed List:  {bucket_time:.6f} seconds")
print(f"Speed Increase: {std_time / bucket_time:.1f}x FASTER\n")


# --- TEST 2: SEARCH BENCHMARK ---
# We will search for 1,000 items.

# Time Standard List
start = time.perf_counter()
for item in search_terms:
    std_list.find(item)
end = time.perf_counter()
std_search_time = end - start

# Time Bucketed List
start = time.perf_counter()
for item in search_terms:
    my_buckets.find(item)
end = time.perf_counter()
bucket_search_time = end - start

print(f"--- SEARCH RESULTS (10000 searches) ---")
print(f"Standard List:  {std_search_time:.6f} seconds")
print(f"Bucketed List:  {bucket_search_time:.6f} seconds")
print(f"Speed Increase: {std_search_time / bucket_search_time:.1f}x FASTER")