import pandas as pd


def split_meal(string, df):
    
    grouped_data = df[df['text'].str.contains(string, case=False)].groupby(df['hour']).size().reset_index(name='count')
    
    dict = {'Breakfast': 0, 'Brunch': 0, 'Lunch': 0, 'Snack': 0, 'Dinner': 0, 'Supper': 0}
    for i, row in grouped_data.iterrows():
        if 5 < grouped_data.loc[i, 'hour'] <= 8:
            dict['Breakfast'] = dict['Breakfast'] + int(grouped_data.loc[i, 'count'])
        if 8 < grouped_data.loc[i, 'hour'] <= 11:
            dict['Brunch'] = dict['Brunch'] + int(grouped_data.loc[i, 'count'])
        if 11 < grouped_data.loc[i, 'hour'] <= 13:
            dict['Lunch'] = dict['Lunch'] + int(grouped_data.loc[i, 'count'])
        if 13 < grouped_data.loc[i, 'hour'] <= 17:
            dict['Snack'] = dict['Snack'] + int(grouped_data.loc[i, 'count'])
        if 17 < grouped_data.loc[i, 'hour'] <= 22:
            dict['Dinner'] = dict['Dinner'] + int(grouped_data.loc[i, 'count'])
        if 22 < grouped_data.loc[i, 'hour'] <= 23 or 0 < grouped_data.loc[i, 'hour'] <= 5:
            dict['Supper'] = dict['Supper'] + int(grouped_data.loc[i, 'count'])        

    return dict