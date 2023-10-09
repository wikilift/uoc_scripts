def update_status_bits(result, status_bits):
    status_bits['Z'] = 1 if result == 0 else 0  # Zero flag
    status_bits['S'] = 1 if (result >> 31) & 1 else 0  # Sign flag
