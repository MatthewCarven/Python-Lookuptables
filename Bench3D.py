import time
import random
import string
import collections

# --- 1. Standard List (The "Control") ---
class StandardList:
    def __init__(self):
        self.data = []
    def add_unique(self, word):
        if word not in self.data:
            self.data.append(word)
    def find(self, word):
        return word in self.data

# --- 2. 1-Layer Bucket (First Letter) ---
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

# --- 3. 2-Layer Bucket (First 2 Letters) ---
class TwoLayerList:
    def __init__(self):
        self.buckets = collections.defaultdict(lambda: collections.defaultdict(list))
    def add_unique(self, word):
        c1, c2 = word[0], word[1]
        if word not in self.buckets[c1][c2]:
            self.buckets[c1][c2].append(word)
    def find(self, word):
        c1, c2 = word[0], word[1]
        if c1 in self.buckets and c2 in self.buckets[c1]:
            return word in self.buckets[c1][c2]
        return False

# --- 4. 3-Layer Bucket (First 3 Letters) ---
class ThreeLayerList:
    def __init__(self):
        # Dictionary -> Dictionary -> Dictionary -> List
        # { 'A': { 'B': { 'C': [words...] } } }
        self.buckets = collections.defaultdict(
            lambda: collections.defaultdict(
                lambda: collections.defaultdict(list)
            )
        )

    def add_unique(self, word):
        c1, c2, c3 = word[0], word[1], word[2]
        # We drill down 3 levels. The final list is tiny.
        target_list = self.buckets[c1][c2][c3]
        
        if word not in target_list:
            target_list.append(word)

    def find(self, word):
        c1, c2, c3 = word[0], word[1], word[2]
        
        # Check Layer 1 -> Layer 2 -> Layer 3
        if (c1 in self.buckets and 
            c2 in self.buckets[c1] and 
            c3 in self.buckets[c1][c2]):
            return word in self.buckets[c1][c2][c3]
        return False

# --- Setup Data (100,000 Items) ---
print("Generating 100,000 initial words (this may take a moment)...")
# Using 6 chars to ensure plenty of unique combinations for the 3rd layer
data_pool = [''.join(random.choices(string.ascii_uppercase, k=6)) for _ in range(100000)]
search_terms = [''.join(random.choices(string.ascii_uppercase, k=6)) for _ in range(1000)]
new_items = [''.join(random.choices(string.ascii_uppercase, k=6)) for _ in range(1000)]

# Initialize lists
std_list = StandardList()
layer1_list = OneLayerList()
layer2_list = TwoLayerList()
layer3_list = ThreeLayerList()

print("Populating databases...")
for word in data_pool:
    std_list.add_unique(word)
    layer1_list.add_unique(word)
    layer2_list.add_unique(word)
    layer3_list.add_unique(word)

print(f"Database populated with {len(std_list.data)} items.\n")

# --- BENCHMARK: INSERT 1,000 NEW ITEMS ---
print(f"--- INSERT BENCHMARK (1,000 items into 100k DB) ---")

# Standard
start = time.perf_counter()
for item in new_items: std_list.add_unique(item)
std_time = time.perf_counter() - start
print(f"Standard List:  {std_time:.6f} s")

# 1-Layer
start = time.perf_counter()
for item in new_items: layer1_list.add_unique(item)
l1_time = time.perf_counter() - start
print(f"1-Layer List:   {l1_time:.6f} s  (Speedup: {std_time/l1_time:.1f}x)")

# 2-Layer
start = time.perf_counter()
for item in new_items: layer2_list.add_unique(item)
l2_time = time.perf_counter() - start
print(f"2-Layer List:   {l2_time:.6f} s  (Speedup: {std_time/l2_time:.1f}x)")

# 3-Layer
start = time.perf_counter()
for item in new_items: layer3_list.add_unique(item)
l3_time = time.perf_counter() - start
print(f"3-Layer List:   {l3_time:.6f} s  (Speedup: {std_time/l3_time:.1f}x)")
print("")

# --- BENCHMARK: SEARCH 1,000 ITEMS ---
print(f"--- SEARCH BENCHMARK (Find 1,000 items in 100k DB) ---")

# Standard
start = time.perf_counter()
for item in search_terms: std_list.find(item)
std_search_time = time.perf_counter() - start
print(f"Standard List:  {std_search_time:.6f} s")

# 1-Layer
start = time.perf_counter()
for item in search_terms: layer1_list.find(item)
l1_search_time = time.perf_counter() - start
print(f"1-Layer List:   {l1_search_time:.6f} s  (Speedup: {std_search_time/l1_search_time:.1f}x)")

# 2-Layer
start = time.perf_counter()
for item in search_terms: layer2_list.find(item)
l2_search_time = time.perf_counter() - start
print(f"2-Layer List:   {l2_search_time:.6f} s  (Speedup: {std_search_time/l2_search_time:.1f}x)")

# 3-Layer
start = time.perf_counter()
for item in search_terms: layer3_list.find(item)
l3_search_time = time.perf_counter() - start
print(f"3-Layer List:   {l3_search_time:.6f} s  (Speedup: {std_search_time/l3_search_time:.1f}x)")