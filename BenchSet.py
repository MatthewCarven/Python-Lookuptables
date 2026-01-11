import time
import collections
import os

# --- 1. Standard List (The "Control") ---
class StandardBinaryList:
    def __init__(self):
        self.data = []
    def add_unique(self, data_chunk):
        if data_chunk not in self.data:
            self.data.append(data_chunk)
    def find(self, data_chunk):
        return data_chunk in self.data

# --- 2. Your 3-Layer Binary Solution ---
class BinaryThreeLayerList:
    def __init__(self):
        self.buckets = collections.defaultdict(
            lambda: collections.defaultdict(
                lambda: collections.defaultdict(list)
            )
        )
    def add_unique(self, data_chunk):
        b1, b2, b3 = data_chunk[0], data_chunk[1], data_chunk[2]
        target_list = self.buckets[b1][b2][b3]
        if data_chunk not in target_list:
            target_list.append(data_chunk)
    def find(self, data_chunk):
        b1, b2, b3 = data_chunk[0], data_chunk[1], data_chunk[2]
        if (b1 in self.buckets and b2 in self.buckets[b1] and b3 in self.buckets[b1][b2]):
            return data_chunk in self.buckets[b1][b2][b3]
        return False

# --- Setup Data (100,000 Items) ---
print("Generating 100,000 binary records...")
# Helper to generate random bytes
def get_random_bytes(length=16): return os.urandom(length)

data_pool = [get_random_bytes() for _ in range(100000)]
search_terms = [get_random_bytes() for _ in range(1000)]
new_items = [get_random_bytes() for _ in range(1000)]

# Initialize containers
std_list = StandardBinaryList()
custom_3layer = BinaryThreeLayerList()
python_set = set() # The Native Challenger

print("Populating databases (Pre-loading 100k items)...")
# Pre-fill
for chunk in data_pool:
    std_list.add_unique(chunk)
    custom_3layer.add_unique(chunk)
    python_set.add(chunk)

print(f"Databases ready.\n")

# --- BENCHMARK: INSERT ---
print("--- INSERT BENCHMARK (1,000 items) ---")

# 1. Standard List
start = time.perf_counter()
for item in new_items: std_list.add_unique(item)
std_time = time.perf_counter() - start

# 2. Your 3-Layer Solution
start = time.perf_counter()
for item in new_items: custom_3layer.add_unique(item)
custom_time = time.perf_counter() - start

# 3. Python Set
start = time.perf_counter()
for item in new_items: 
    python_set.add(item) # set.add handles uniqueness automatically
set_time = time.perf_counter() - start

print(f"Standard List:  {std_time:.6f} s")
print(f"Your Solution:  {custom_time:.6f} s")
print(f"Python Set:     {set_time:.6f} s")
print("-" * 30)
print(f"Your Speedup vs List: {std_time / custom_time:.1f}x")
print(f"Set Speedup vs List:  {std_time / set_time:.1f}x")
print("")

# --- BENCHMARK: SEARCH ---
print("--- SEARCH BENCHMARK (1,000 items) ---")

# 1. Standard List
start = time.perf_counter()
for item in search_terms: std_list.find(item)
std_search_time = time.perf_counter() - start

# 2. Your 3-Layer Solution
start = time.perf_counter()
for item in search_terms: custom_3layer.find(item)
custom_search_time = time.perf_counter() - start

# 3. Python Set
start = time.perf_counter()
for item in search_terms: 
    _ = item in python_set
set_search_time = time.perf_counter() - start

print(f"Standard List:  {std_search_time:.6f} s")
print(f"Your Solution:  {custom_search_time:.6f} s")
print(f"Python Set:     {set_search_time:.6f} s")
print("-" * 30)
print(f"Your Speedup vs List: {std_search_time / custom_search_time:.1f}x")
print(f"Set Speedup vs List:  {std_search_time / set_search_time:.1f}x")