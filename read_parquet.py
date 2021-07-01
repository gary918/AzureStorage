
# -*- coding:utf-8 -*-
import pandas as pd
import pyarrow
df = pd.read_parquet('./sample.parquet', engine='pyarrow')
print(len(df.index))
print(df)