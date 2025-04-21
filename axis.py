import pandas as pd

def axis_1(df):
    return df.sum(axis=1)

def axis_0(df):
    return df.sum(axis=0)

# if __name__=="__main__":
#     df = pd.DataFrame([[1,3],[2,4],[3,5],[4,6]])
#     result0 = axis_1(df, axis=0)
#     result1 = axis_1(df, axis=1)
#     print(result0)
#     print(result0.shape[0])
#     print("\n")
#     print(result1)