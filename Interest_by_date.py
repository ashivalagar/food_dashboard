import pandas as pd


def group_by_date(string, df):
    df['date'] = pd.to_datetime(df['date'], unit='D')  # Convert date to Timestamp to group by month
    df = df[~(df['date'] < '2018-12-31')]  # Drop data before year 2019
    
    grouped_data = df[df['text'].str.contains(string, case=False)].groupby(df['date'].dt.floor('30D')).size().reset_index(name='count')
    
    # Change date to "mm-YYYY" format
    for i, row in grouped_data.iterrows():
        grouped_data.loc[i, 'date'] = str(grouped_data.loc[i, 'date'].month) + "-" + str(grouped_data.loc[i, 'date'].year)
    
    return grouped_data.to_dict(orient='record')