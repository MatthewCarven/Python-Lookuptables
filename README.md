Um like this is memory greedy disk based lookup prediction, I.E. you tell me what are the beginning 3 bytes and I feed back to you all the possibilities in close to N(1) time

<img width="468" height="221" alt="image" src="https://github.com/user-attachments/assets/937de5d1-ab67-4270-95aa-87a64f7bfef6" />



## C# port

There is a C# / .NET 10 port of these lookup tables, benchmarked against the built-in .NET collections (`HashSet`, `FrozenSet`, sorted lists and more), at [CSharp-Lookuptables](https://github.com/MatthewCarven/CSharp-Lookuptables).

### 64 GB disk test

The C# port of `BenchDisk2.py` was run on a 64 GB database: 1,048,592 records of 64 KB each, stored as a flat file plus the 3-byte bucket index, 128 GB in total. That's 8x the test machine's 15.8 GB of RAM, so neither the OS file cache nor the SSD's own cache could hold it, and the reads came off the SSD.

| Method | Per lookup | All 131,070 lookups |
|---|--:|--:|
| Bucket index (open one small file, read ~64 KB) | **0.36 ms** | 47 s |
| Full scan of the flat file (~910 MB/s) | 42.7 s | ~1,554 hours (projected) |

That's about **118,000x faster** than scanning. Half the lookups were hits, spread across every record on disk. Full results and method: [CSharp-Lookuptables disk results](https://github.com/MatthewCarven/CSharp-Lookuptables/blob/main/results/csharp-disk.md).
