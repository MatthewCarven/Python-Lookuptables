import time
import collections
import os

# --- 1. Standard List ---
class StandardBinaryList:
    def __init__(self):
        self.data = []
    def add_unique(self, data_chunk):
        if data_chunk not in self.data:
            self.data.append(data_chunk)
    def find(self, data_chunk):
        return data_chunk in self.data

# --- 2. 3-Layer Solution ---
class ThreeLayerList:
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

# --- 3. 4-Layer Solution ---
class FourLayerList:
    def __init__(self):
        self.buckets = collections.defaultdict(
            lambda: collections.defaultdict(
                lambda: collections.defaultdict(
                    lambda: collections.defaultdict(list)
                )
            )
        )
    def add_unique(self, data_chunk):
        b1, b2, b3, b4 = data_chunk[0], data_chunk[1], data_chunk[2], data_chunk[3]
        target_list = self.buckets[b1][b2][b3][b4]
        if data_chunk not in target_list:
            target_list.append(data_chunk)
    def find(self, data_chunk):
        b1, b2, b3, b4 = data_chunk[0], data_chunk[1], data_chunk[2], data_chunk[3]
        if (b1 in self.buckets and 
            b2 in self.buckets[b1] and 
            b3 in self.buckets[b1][b2] and
            b4 in self.buckets[b1][b2][b3]):
            return data_chunk in self.buckets[b1][b2][b3][b4]
        return False

# --- Setup Data (100,000 Items) ---
print("Generating 100,000 binary records...")
def get_random_bytes(length=16): return os.urandom(length)

data_pool = [get_random_bytes() for _ in range(100000)]
search_terms = [get_random_bytes() for _ in range(1000)]
new_items = [get_random_bytes() for _ in range(1000)]

# Initialize
std_list = StandardBinaryList()
layer3_list = ThreeLayerList()
layer4_list = FourLayerList()
python_set = set()

print("Populating databases...")
for chunk in data_pool:
    std_list.add_unique(chunk)
    layer3_list.add_unique(chunk)
    layer4_list.add_unique(chunk)
    python_set.add(chunk)

print(f"Databases ready.\n")

# --- BENCHMARK: INSERT ---
print("--- INSERT BENCHMARK (1,000 items) ---")

start = time.perf_counter()
for item in new_items: std_list.add_unique(item)
std_time = time.perf_counter() - start

start = time.perf_counter()
for item in new_items: layer3_list.add_unique(item)
l3_time = time.perf_counter() - start

start = time.perf_counter()
for item in new_items: layer4_list.add_unique(item)
l4_time = time.perf_counter() - start

start = time.perf_counter()
for item in new_items: python_set.add(item)
set_time = time.perf_counter() - start

print(f"Standard List:  {std_time:.6f} s")
print(f"3-Layer List:   {l3_time:.6f} s")
print(f"4-Layer List:   {l4_time:.6f} s")
print(f"Python Set:     {set_time:.6f} s")
print("")


# --- BENCHMARK: SEARCH ---
print("--- SEARCH BENCHMARK (1,000 items) ---")

start = time.perf_counter()
for item in search_terms: std_list.find(item)
std_search_time = time.perf_counter() - start

start = time.perf_counter()
for item in search_terms: layer3_list.find(item)
l3_search_time = time.perf_counter() - start

start = time.perf_counter()
for item in search_terms: layer4_list.find(item)
l4_search_time = time.perf_counter() - start

start = time.perf_counter()
for item in search_terms: _ = item in python_set
set_search_time = time.perf_counter() - start

print(f"Standard List:  {std_search_time:.6f} s")
print(f"3-Layer List:   {l3_search_time:.6f} s")
print(f"4-Layer List:   {l4_search_time:.6f} s")
print(f"Python Set:     {set_search_time:.6f} s")