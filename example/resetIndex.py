import pandas as pd
import numpy as np

def resetIndex(df, category):
    return df.groupby(category).sum().reset_index()

def no_resetIndex(df, category):
    return df.groupby(category).sum()

