import pandas as pd
import numpy as np

authors = pd.read_excel('authors.xlsx', index_col=0)

data = np.random.randint(1,10,size=200)
df = pd.DataFrame(data, columns=['author'])
data2 = np.random.randint(1,136,size=200)
df['books'] = data2
print(df.iloc[3]['author'])
for x in df.itertuples():
    print(x[1], x[2])
