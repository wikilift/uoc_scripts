def update_cache_lru(access_sequence, cache_size, block_size):
    err_cnt = 0
    cache = {i: None for i in range(cache_size)}
    lru_counter = {i: 0 for i in range(cache_size)}

    cache_fails_output = []

    def calculate_block_number(address):
        return address // block_size

    for access in access_sequence:
        block_number = calculate_block_number(access)
        found = False

        for l in lru_counter:
            lru_counter[l] += 1

 
        for line, block in cache.items():
            if block == block_number:
                found = True
                lru_counter[line] = 0
                break

        if not found:
            lru_line = max(lru_counter, key=lru_counter.get)
            cache[lru_line] = block_number
            cache_fails_output.append((access, lru_line, block_number))
            err_cnt += 1
            lru_counter[lru_line] = 0


    formatted_lru_fails = ["Fallo:{} {}({}-{})".format(fail[0], fail[1], fail[2]*block_size, fail[2]*block_size + block_size - 1) for fail in cache_fails_output]
    ok = len(access_sequence) - err_cnt
    hit_ratio = ok / len(access_sequence)
    time_succes = 4  
    time_fault = 20  
    tm = time_succes * hit_ratio + time_fault * (1 - hit_ratio)

    print(f"La tasa de aciertos (Hit Ratio) es: {hit_ratio}")
    print(f"El tiempo de acceso a memoria medio es: {tm}ns")
    print("Done!")
    return formatted_lru_fails



access_sequence = [0, 1, 2, 13, 14, 15, 16, 37, 38, 23, 24, 25, 42, 17, 18, 53, 54, 55, 56, 20, 21, 15, 16]
cache_size = 3
block_size = 8

formatted_lru_fails = update_cache_lru(access_sequence, cache_size, block_size)
for x in formatted_lru_fails:
    print(x)