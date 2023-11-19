from memory_ops import translate_to_hex_with_labels



    
def printResult(offset,graphic=False,xlsOutput=False):
    import pandas as pd
    hex_translation_reduced = translate_to_hex_with_labels(instructions= program,memory_values= memory_values, offset=offset)
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

memory_values= {
    "V": "00800080",
    "B": "200",
    "100":"0"
}
initial_offset=0x00AABBCC

program = [
    ('XOR', 'R10', '[V]','LABEL:E1'),
    ('ADD', 'R10','[R1]' ),
    ('CMP', 'R10',10),
    ('JLE', 'E1'),
    ('SUB', 'R10', '[V+R1]'),
   
]



printResult(xlsOutput=True,graphic=True,offset=initial_offset)




