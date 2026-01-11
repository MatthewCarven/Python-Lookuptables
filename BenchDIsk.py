import os
import time
import random

# --- Configuration ---
DB_ROOT = "my_database_index"
RECORD_SIZE = 65535  # 64KB per record
TOTAL_RECORDS = 250000 # ~16 GB Total

# --- 1. The Disk Indexer ---
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
        with open(file_path, "rb") as f:
            while True:
                record = f.read(RECORD_SIZE)
                if not record: break
                if record == data_chunk: return True
        return False

# --- 2. The Linear Search ---
def linear_disk_search(target, all_data_file):
    with open(all_data_file, "rb") as f:
        while True:
            record = f.read(RECORD_SIZE)
            if not record: break
            if record == target: return True
    return False

# --- SETUP ---
print(f"--- 16GB STREAMING DEMO ---")
print(f"Record Size: {RECORD_SIZE} bytes")
print(f"Total Records: {TOTAL_RECORDS}")
print(f"Est. Total Size: {TOTAL_RECORDS * RECORD_SIZE / (1024**3):.2f} GB")

indexer = DiskIndexer(DB_ROOT)
flat_file_path = "huge_flat_file.bin"

# Pick a random index to be our "Target"
target_index = random.randint(0, TOTAL_RECORDS - 1)
target_item = None # We will capture this during the loop

print("\nStarting Stream: Generate -> Index -> Write Flat File...")
start_time = time.perf_counter()

# Open the flat file once and append to it as we go
with open(flat_file_path, "wb") as f_flat:
    for i in range(TOTAL_RECORDS):
        # 1. Generate ONE chunk (64KB RAM usage)
        chunk = os.urandom(RECORD_SIZE)
        
        # 2. Capture it if it's the one we want to search for later
        if i == target_index:
            target_item = chunk
            print(f"  [Target Item Selected at index {i}]")
            
        # 3. Add to Flat File (Control Group)
        f_flat.write(chunk)
        
        # 4. Add to Index (Your Logic)
        indexer.add(chunk)
        
        # 5. Loop repeats, 'chunk' is overwritten/garbage collected. 
        # RAM never grows.
        
        if i % 10000 == 0:
            print(f"  Processed {i} records...")

print(f"Generation Complete. Time: {time.perf_counter() - start_time:.2f}s")

# --- STABILIZE ---
print("\nPausing 5s for OS Write Buffers...")
time.sleep(5)

# --- BENCHMARK ---
print("\n--- SEARCH BENCHMARK ---")

# 1. Indexed Search
print("Running Indexed Search...")
start = time.perf_counter()
found_index = indexer.find(target_item)
index_time = time.perf_counter() - start
print(f"Indexed Search:   {index_time:.6f} s  (Result: {found_index})")

# 2. Linear Scan
# WARNING: This will actually read 16GB from disk. It might take a minute or two.
print("Running Linear Scan (This might take a while)...")
start = time.perf_counter()
found_linear = linear_disk_search(target_item, flat_file_path)
linear_time = time.perf_counter() - start
print(f"Linear File Scan: {linear_time:.6f} s  (Result: {found_linear})")

if index_time > 0:
    print(f"\nSpeedup: {linear_time / index_time:.1f}x FASTER")