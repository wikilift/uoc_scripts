
def cache_associative(memory_accesses):
    def calculate_block_number(address):
        return address // 8

    cache = [None, None, None]


    cache_fails_output = []

    fail_count = 0

    for access in memory_accesses:
        block_number = calculate_block_number(access)
        if block_number not in cache:
            replace_position = fail_count % len(cache)
            cache[replace_position] = block_number
            fail_info = f"Fallo:{access} {replace_position}({block_number*8}-{block_number*8+7})"
            cache_fails_output.append(fail_info)
            fail_count += 1

    for x in cache_fails_output:
        print(x)

    ok=len(memory_accesses)-fail_count
    hit_ratio = ok/ len(memory_accesses)
    time_succes = 4  
    time_fault = 20  
    tm = time_succes * hit_ratio + time_fault * (1 - hit_ratio)
    print(f"La tasa de aciertos (Hit Ratio) es: {hit_ratio}")
    print(f"El tiempo de acceso a memoria medio es: {tm}ns")
    print("Done!")
    
memory_accesses = [0, 1, 2, 13, 14, 15, 16, 37, 38, 23, 24, 25, 42, 17, 18, 53, 54, 55, 56, 20, 21, 15, 16]
cache_associative(memory_accesses=memory_accesses)