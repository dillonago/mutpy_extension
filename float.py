import numpy as np
import pandas as pd

def floatMul(df, num):
    df_mul = df * np.float32(num)
    return df_mul

def comMul(df, num):
    df_com = df * np.complex64(num)
    return df_com