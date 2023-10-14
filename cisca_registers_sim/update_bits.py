label_positions={}
status_bits = {
        'Z': 0,
        'S': 0,
        'C': 0,
        'V': 0
    }
def set_labels(program):
    for idx, (instruction, *operands) in enumerate(program):
        if instruction == 'LABEL':
            label_positions[operands[0]] = idx
    return label_positions
   
def update_status_bits(result,reset=False):
    status_bits['Z'] = 1 if result == 0 else 0  
    status_bits['S'] = 1 if (result >> 31) & 1 else 0 
    if reset :
        status_bits['C'] =  0 
        status_bits['V'] =  0 

    

def JE(label, index):
    
    if status_bits['Z'] == 1:
        return label_positions[label]
    return index

def JNE(label, index):
    if status_bits['Z'] == 0: 
        return label_positions[label]
    return index

def JGE(label, index):
    if status_bits['S'] == 0: 
        return label_positions[label]
    return index

def JG(label, index):
    if status_bits['S'] == 0 and status_bits['Z'] == 0: 
        return label_positions[label]
    return index

def JLE(label, index):
    if status_bits['S'] == 1 or status_bits['Z'] == 1:  
        return label_positions[label]
    return index

def JL(label, index):
    if status_bits['S'] == 1:  
        return label_positions[label]
    return index