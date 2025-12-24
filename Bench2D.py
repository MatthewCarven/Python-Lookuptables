import time
import random
import string
import collections

# --- 1. Standard List (O(N)) ---
class StandardList:
    def __init__(self):
        self.data = []
    def add_unique(self, word):
        if word not in self.data:
            self.data.append(word)
    def find(self, word):
        return word in self.data

# --- 2. 1-Layer Bucket (O(N/26)) ---
class OneLayerList:
    def __init__(self):
        self.buckets = collections.defaultdict(list)
    def add_unique(self, word):
        c1 = word[0]
        if word not in self.buckets[c1]:
            self.buckets[c1].append(word)
    def find(self, word):
        c1 = word[0]
        if c1 in self.buckets:
            return word in self.buckets[c1]
        return False

# --- 3. 2-Layer Bucket (O(N/676)) ---
class TwoLayerList:
    def __init__(self):
        # A dictionary of dictionaries of lists
        # Structure: { 'A': { 'A': [words...], 'B': [words...] } }
        self.buckets = collections.defaultdict(lambda: collections.defaultdict(list))
        
    def add_unique(self, word):
        c1 = word[0]
        c2 = word[1] # "Second Dimension"
        
        # We only scan the tiny list inside the second bucket
        if word not in self.buckets[c1][c2]:
            self.buckets[c1][c2].append(word)
            
    def find(self, word):
        c1 = word[0]
        c2 = word[1]
        
        # Check Layer 1, then Layer 2
        if c1 in self.buckets and c2 in self.buckets[c1]:
            return word in self.buckets[c1][c2]
        return False

# --- Setup Data ---
# We need more data to really show the power of the 2-layer system
# Let's bump the database to 50,000 words so the "search piles" are significant.
print("Generating 50,000 initial words...")
data_pool = [''.join(random.choices(string.ascii_uppercase, k=5)) for _ in range(50000)]
search_terms = [''.join(random.choices(string.ascii_uppercase, k=5)) for _ in range(10000)]
new_items = [''.join(random.choices(string.ascii_uppercase, k=5)) for _ in range(10000)]

std_list = StandardList()
layer1_list = OneLayerList()
layer2_list = TwoLayerList()

# Populate initial DB
for word in data_pool:
    std_list.add_unique(word)
    layer1_list.add_unique(word)
    layer2_list.add_unique(word)

print(f"Database populated with {len(std_list.data)} items.\n")

# --- BENCHMARK: INSERT 1,000 NEW ITEMS ---
print("--- INSERT BENCHMARK (Checking uniqueness for 10,000 new items) ---")

# Standard
start = time.perf_counter()
for item in new_items: std_list.add_unique(item)
std_time = time.perf_counter() - start

# 1-Layer
start = time.perf_counter()
for item in new_items: layer1_list.add_unique(item)
l1_time = time.perf_counter() - start

# 2-Layer
start = time.perf_counter()
for item in new_items: layer2_list.add_unique(item)
l2_time = time.perf_counter() - start

print(f"Standard List:  {std_time:.6f} s")
print(f"1-Layer List:   {l1_time:.6f} s  ({std_time/l1_time:.1f}x faster)")
print(f"2-Layer List:   {l2_time:.6f} s  ({std_time/l2_time:.1f}x faster)")
print("")

# --- BENCHMARK: SEARCH 1,000 ITEMS ---
print("--- SEARCH BENCHMARK (Looking up 10,000 items) ---")

# Standard
start = time.perf_counter()
for item in search_terms: std_list.find(item)
std_search_time = time.perf_counter() - start

# 1-Layer
start = time.perf_counter()
for item in search_terms: layer1_list.find(item)
l1_search_time = time.perf_counter() - start

# 2-Layer
start = time.perf_counter()
for item in search_terms: layer2_list.find(item)
l2_search_time = time.perf_counter() - start

print(f"Standard List:  {std_search_time:.6f} s")
print(f"1-Layer List:   {l1_search_time:.6f} s  ({std_search_time/l1_search_time:.1f}x faster)")
print(f"2-Layer List:   {l2_search_time:.6f} s  ({std_search_time/l2_search_time:.1f}x faster)")