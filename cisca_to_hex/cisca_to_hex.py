from memory_ops import translate_to_hex_with_labels




def printResult(graphic=False,xlsOutput=False):
    import pandas as pd
    hex_translation_reduced = translate_to_hex_with_labels(program, memory_values, initial_offset=0x00010000)
    df = pd.DataFrame(list(hex_translation_reduced.items()), columns=['Offset', 'Hex Translation'])
    split_data = df['Hex Translation'].str.split('\t', expand=True)
    split_data.columns = ['Instruction', 'Hex Code']
    df = pd.concat([df['Offset'], split_data], axis=1)
    max_len = df['Hex Code'].str.len().max()
    df['Hex Code'] = df['Hex Code'].apply(lambda x: x.ljust(max_len) if x else "")
    print(df)
    if graphic :
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(12, 4)) 
        ax.axis('tight')
        ax.axis('off')
        ax.table(cellText=df.values, colLabels=df.columns, cellLoc = 'left', loc='center')
        plt.show()
    if xlsOutput :
        import os
        output_folder = "output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        excel_path = os.path.join(output_folder, "translated_instructions.xlsx")
        df.to_excel(excel_path, index=False)

#exercice 1
program = [
    ('MOV', 'R1', 'R2'),
    ('DEC', 'R2', 'LABEL:E1'),
    ('JE', 'E2'),
    ('MUL', 'R1', 'R2'),
    ('JMP', 'E1'),
    ('MOV', 'R3', 4, 'LABEL:E2'),
    ('MOV', '[100+R3]', 'R1')
]

# # #! exercice 2
# program = [
#     ('MOV', 'R0', '[A]'),
#     ('CMP', 'R0', '[B]'),
#     ('JLE', 'E1'),
#     ('DEC', 'R0'),
#     ('JMP', 'E2'),
#     ('ADD', '[B]', 4, 'LABEL:E1'),
#     ('MUL', '[B]', 'R0', 'LABEL:E2'),
#     ('MOV', '[A]', 'R0'),
   
# ]
memory_values= {
    "A": "20",
    "B": "200",
    "100":"0"
}
printResult(xlsOutput=False,graphic=False)


