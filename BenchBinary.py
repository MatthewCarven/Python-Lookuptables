import time
import random
import collections
import os

# --- 1. Standard List (Control) ---
class StandardBinaryList:
    def __init__(self):
        self.data = []
    def add_unique(self, data_chunk):
        if data_chunk not in self.data:
            self.data.append(data_chunk)
    def find(self, data_chunk):
        return data_chunk in self.data

# --- 2. 3-Layer Binary Lookup (Base-256) ---
class BinaryThreeLayerList:
    def __init__(self):
        # Layer 1 -> Layer 2 -> Layer 3 -> List
        # Keys are now Integers (0-255) rather than Characters
        self.buckets = collections.defaultdict(
            lambda: collections.defaultdict(
                lambda: collections.defaultdict(list)
            )
        )

    def add_unique(self, data_chunk):
        # Extract first 3 bytes (0-255)
        # Note: In Python, indexing a bytes object returns the integer value directly
        b1, b2, b3 = data_chunk[0], data_chunk[1], data_chunk[2]
        
        target_list = self.buckets[b1][b2][b3]
        
        # Scan the tiny final list
        if data_chunk not in target_list:
            target_list.append(data_chunk)

    def find(self, data_chunk):
        b1, b2, b3 = data_chunk[0], data_chunk[1], data_chunk[2]
        
        if (b1 in self.buckets and 
            b2 in self.buckets[b1] and 
            b3 in self.buckets[b1][b2]):
            return data_chunk in self.buckets[b1][b2][b3]
        return False

# --- Setup Binary Data (100,000 items) ---
print("Generating 100,000 binary records (16 bytes each)...")

# Helper to generate random bytes
def get_random_bytes(length=16):
    return os.urandom(length)

# Generate Data
data_pool = [get_random_bytes() for _ in range(100000)]
search_terms = [get_random_bytes() for _ in range(1000)]
new_items = [get_random_bytes() for _ in range(1000)]

std_list = StandardBinaryList()
binary_3layer = BinaryThreeLayerList()

print("Populating databases...")
for chunk in data_pool:
    std_list.add_unique(chunk)
    binary_3layer.add_unique(chunk)

print(f"Database populated with {len(std_list.data)} items.\n")

# --- BENCHMARK: INSERT ---
print("--- INSERT BENCHMARK (Binary) ---")

# Standard
start = time.perf_counter()
for item in new_items: std_list.add_unique(item)
std_time = time.perf_counter() - start

# 3-Layer Binary
start = time.perf_counter()
for item in new_items: binary_3layer.add_unique(item)
bin_time = time.perf_counter() - start

print(f"Standard List:  {std_time:.6f} s")
print(f"3-Layer Binary: {bin_time:.6f} s")
print(f"Speed Increase: {std_time / bin_time:.1f}x FASTER\n")


# --- BENCHMARK: SEARCH ---
print("--- SEARCH BENCHMARK (Binary) ---")

# Standard
start = time.perf_counter()
for item in search_terms: std_list.find(item)
std_search_time = time.perf_counter() - start

# 3-Layer Binary
start = time.perf_counter()
for item in search_terms: binary_3layer.find(item)
bin_search_time = time.perf_counter() - start

print(f"Standard List:  {std_search_time:.6f} s")
print(f"3-Layer Binary: {bin_search_time:.6f} s")
print(f"Speed Increase: {std_search_time / bin_search_time:.1f}x FASTER")