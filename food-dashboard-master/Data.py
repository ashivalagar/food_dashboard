import pandas as pd

def get_data(path_name):
    df = pd.read_json(path_name)
    return df
