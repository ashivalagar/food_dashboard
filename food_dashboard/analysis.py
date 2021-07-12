from typing import Counter
import pandas as pd
import stemming 
import os
import sys
import requests
sys.path.append('/home/sun/food_dashboard/food-dashboard-master')
import Percentage
import Interest_by_date
import Data
#paths
paths=['../raw_dataset/cleaned_menu_links.csv','../raw_dataset/cleaned_packaged_foods.csv','../raw_dataset/cleaned_receipe.csv']

def word_count(word):
    
    counter =[]
    counter_old = []
    for path in paths:
        df = pd.read_csv(path)
        dict = {}
        file_name = path.split('/')[-1]
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

        df['date'] = df['date'].apply(lambda x: "%d/%d" % (x.week, x.year))
        unique_dates=df['date'].unique()
        unique_dates[::-1].sort()
        count = 0
        count_old= 0
        
        is_date = df['date'] == unique_dates[0]
        temp_df = df[is_date]
        count = temp_df['food name'].str.contains(word,case=False).sum()
        try:
            is_date = df['date'] == unique_dates[1]
            temp_df = df[is_date]
            count_old = temp_df['food name'].str.contains(word).sum()
        except:
            pass 

        print(count)
        counter_old.append(count_old/len(df)*100)
        counter.append(count/len(df)*100)
        
        if(count_old != 0):
            percentage_change = count-count_old/count_old*100
        else:
            percentage_change = 0
    insta = pd.read_csv('../raw_dataset/cleaned_instagram.csv')
    insta_percent = Percentage.percentage(word, insta, 'text')
    counter.append(insta_percent)

     
    return counter,percentage_change



def line_graph(word,path,attr):       
        
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])  # Convert date to Timestamp to group by month
    df = df[~(df['date'] < '2018-12-31')]  # Drop data before year 2019
    
    grouped_data = df[df[attr].str.contains(word, case=False)].groupby(df['date'].dt.floor('30D')).size().reset_index(name='count')
    
    # Change date to "mm-YYYY" format
    for i, row in grouped_data.iterrows():
        grouped_data.loc[i, 'date'] = str(grouped_data.loc[i, 'date'].week) + "-" + str(grouped_data.loc[i, 'date'].year)
    
    return grouped_data.to_dict(orient='record')



word=input("give word")
word=word.lower()
word=stemming.stemming([word])[0]
print(word_count(word))
line_receipe=line_graph(word,paths[2],'food name')
line_packagedfoods=line_graph(word,paths[1],'food name')
line_menulinks=line_graph(word,paths[0],'food name')
line_instagram=line_graph(word,'../raw_dataset/cleaned_instagram.csv','text')

print('menu_links:',line_menulinks)
print('packaged:',line_packagedfoods)
print('receipe:',line_receipe)
print('instagram:',line_instagram)



