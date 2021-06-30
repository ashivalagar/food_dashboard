import pandas as pd


def percentage(string, df, attr):
    n = df.shape[0]
    row_count = df[df[attr].str.contains(string, case=False)].shape[0]
    percentage = row_count/n * 100
    return percentage