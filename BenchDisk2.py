import os
import time
import random

# --- Configuration ---
DB_ROOT = "my_database_index"
RECORD_SIZE = 65535      # 64KB per record
TOTAL_RECORDS = 250000   # ~16 GB Total Database
BATCH_SIZE = 1024        # Read 1024 records at once for Linear Scan (~67MB)
LOOKUP_COUNT = 131070    # How many lookups to perform per method

# --- 1. The Disk Indexer (O(1) Logic) ---
class DiskIndexer:
    def __init__(self, root_dir):
        self.root = root_dir
        if not os.path.exists(self.root):
            os.makedirs(self.root)
            
    def _get_path(self, data_chunk):
        d1 = f"{data_chunk[0]:02x}"
        d2 = f"{data_chunk[1]:02x}"
        d3 = f"{data_chunk[2]:02x}"
        folder_path = os.path.join(self.root, d1, d2)
        file_path = os.path.join(folder_path, f"bucket_{d3}.bin")
        return folder_path, file_path

    def add(self, data_chunk):
        folder_path, file_path = self._get_path(data_chunk)
        os.makedirs(folder_path, exist_ok=True)
        with open(file_path, "ab") as f:
            f.write(data_chunk)
            
    def find(self, data_chunk):
        _, file_path = self._get_path(data_chunk)
        if not os.path.exists(file_path): return False
        
        # Read the bucket. Since buckets are small, we read the whole thing.
        # This is effectively "Batch Reading" for the indexer too.
        with open(file_path, "rb") as f:
            while True:
                record = f.read(RECORD_SIZE)
                if not record: break
                if record == data_chunk: return True
        return False

# --- 2. The Batched Linear Scan (Optimized O(N)) ---
def linear_disk_search_batched(target, all_data_file):
    with open(all_data_file, "rb") as f:
        while True:
            # READ IN BATCHES (The Optimization)
            # Read 64MB at once instead of 64KB
            chunk_batch = f.read(RECORD_SIZE * BATCH_SIZE)
            if not chunk_batch: break
            
            # If the target is in this massive byte chunk, we found it.
            # Note: exact match in bytes is faster than splitting loops
            if target in chunk_batch:
                return True
    return False

# --- SETUP ---
print(f"--- 16GB HIGH-LOAD STRESS TEST ---")
print(f"Total Records: {TOTAL_RECORDS}")
print(f"Lookups to Perform: {LOOKUP_COUNT}")
print(f"Linear Read Batch: {BATCH_SIZE} records ({BATCH_SIZE * RECORD_SIZE / 1024 / 1024:.2f} MB)")

indexer = DiskIndexer(DB_ROOT)
flat_file_path = "huge_flat_file.bin"

# We need a list of targets to search for later
# We'll pick 10 random existing items to search for repeatedly
# (Searching for 131,070 *unique* items would require storing them all in RAM, which crashes us)
known_targets = [] 

print("\n--- PHASE 1: GENERATION (Streaming) ---")
start_time = time.perf_counter()

with open(flat_file_path, "wb") as f_flat:
    for i in range(TOTAL_RECORDS):
        chunk = os.urandom(RECORD_SIZE)
        
        # Capture a few targets for our lookup test
        if len(known_targets) < 100 and random.random() < 0.01:
            known_targets.append(chunk)
            
        f_flat.write(chunk)
        indexer.add(chunk)
        
        if i % 50000 == 0:
            print(f"  Processed {i} records...")

print(f"Generation Complete. Time: {time.perf_counter() - start_time:.2f}s")
print(f"captured {len(known_targets)} known targets for testing.")

# --- STABILIZE ---
print("\nPausing 5s for OS Write Buffers...")
time.sleep(5)

# --- GENERATE LOOKUP LIST ---
# We create a list of 131,070 items to search for.
# 50% will be Real Targets (Hits), 50% will be Random Junk (Misses)
lookup_list = []
for _ in range(LOOKUP_COUNT):
    if random.random() > 0.5:
        lookup_list.append(random.choice(known_targets)) # Should return True
    else:
        lookup_list.append(os.urandom(RECORD_SIZE))      # Should return False

print(f"\n--- PHASE 2: BENCHMARK ({LOOKUP_COUNT} Accesses) ---")

# 1. Indexed Search Benchmark
print(f"Starting Indexed Search (x{LOOKUP_COUNT})...")
start = time.perf_counter()
hits = 0
for item in lookup_list:
    if indexer.find(item):
        hits += 1
index_time = time.perf_counter() - start
print(f"Indexed Total Time: {index_time:.4f}s")
print(f"Avg Time per Lookup: {index_time/LOOKUP_COUNT*1000:.4f} ms")
print(f"Hits found: {hits}")

# 2. Linear Search Benchmark
# CRITICAL NOTE: Doing 131,070 linear scans of a 16GB file is physically impossible
# in a reasonable time (it would take years).
# We will run just *5* full scans to get an average, then project the math.
print("\nStarting Linear Search (Running 5 samples to estimate total time)...")
linear_samples = 5
start = time.perf_counter()
for i in range(linear_samples):
    item = lookup_list[i]
    linear_disk_search_batched(item, flat_file_path)
    print(f"  Linear Scan {i+1}/{linear_samples} complete...")

linear_sample_time = time.perf_counter() - start
avg_linear_time = linear_sample_time / linear_samples
projected_linear_time = avg_linear_time * LOOKUP_COUNT

print(f"\n--- RESULTS ---")
print(f"Indexed Time (Actual):      {index_time:.2f} seconds")
print(f"Linear Time (Projected):    {projected_linear_time:.2f} seconds ({projected_linear_time/3600:.2f} hours)")
print(f"Speedup Factor:             {projected_linear_time / index_time:.0f}x FASTER")