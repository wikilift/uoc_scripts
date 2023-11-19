### Memory Cache - Python Implementations

🧠📦 This repository contains implementations of different memory cache strategies in the Python programming language. The three implementations are:

1. **LRU Cache (Least Recently Used)**: This module, `memory_cache_lru.py`, implements an LRU cache that is updated based on a memory access sequence. You can configure the cache size and block size as needed.

2. **Direct Mapping Cache**: The `memory_cache_direct_assing.py` file contains an implementation of a direct mapping cache. You can specify the block size and the number of cache lines you want to use.

3. **Associative Cache**: In `memory_cache_associative.py`, you'll find an implementation of an associative cache. This cache replaces memory blocks based on the access sequence.

### Usage

Here's how you can use each of these implementations:

### LRU Cache

```python
from memory_cache_lru import update_cache_lru

access_sequence = [0, 1, 2, 13, 14, 15, 16, 37, 38, 23, 24, 25, 42, 17, 18, 53, 54, 55, 56, 20, 21, 15, 16]
cache_size = 3
block_size = 8

formatted_lru_fails = update_cache_lru(access_sequence, cache_size, block_size)
for x in formatted_lru_fails:
    print(x)
```

### Direct Mapping Cache

```python
from memory_cache_direct_assing import direct_assign

memory_accesses = [1, 2, 13, 14, 26, 27, 28, 29, 36, 37, 38, 39, 40, 3, 10, 11, 12, 13, 14, 15, 30, 8, 12]
block_size = 4
num_lines = 4

direct_assign(initial_state=True, block_size=block_size, num_lines=num_lines, memory_accesses=memory_accesses)

```
### Associative Cache

```python
from memory_cache_associative import cache_associative

memory_accesses = [0, 1, 2, 13, 14, 15, 16, 37, 38, 23, 24, 25, 42, 17, 18, 53, 54, 55, 56, 20, 21, 15, 16]
cache_associative(memory_accesses=memory_accesses)

```

### Each implementation file contains a specific function that you can use according to your needs. Make sure to adjust parameters such as cache size, block size, and memory access sequence according to your requirements.

### License 📜

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify the code for your educational purposes.
