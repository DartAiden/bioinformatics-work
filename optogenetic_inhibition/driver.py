import pandas as pd
import os
df = pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sample.xlsx'))
threshold = float(input("Please enter the threshold value you would like to use. "))
lst = []
for index, row in df.iterrows():
    count = 0
    for c in range(23, len(row)):
        if row[c] > threshold:
            count+=1
    lst.append(count)
output = pd.DataFrame(lst)
output.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output.xlsx'), index=True)
print("Output successfully printed")
