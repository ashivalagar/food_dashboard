from typing import Counter
import pandas as pd
import stemming 
import os
import sys
sys.path.append('food_dashboard/')
import requests
import Percentage
import Interest_by_date
import Data
#paths
paths=['raw_dataset/cleaned_menu_links.csv','raw_dataset/cleaned_packaged_foods.csv','raw_dataset/cleaned_receipe.csv']

def word_count(word):
    count_no = []
    counter =[]
    counter_old = []
    percentage_changer=[]
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
        count = temp_df['text'].str.contains(word,case=False).sum()
        try:
            is_date = df['date'] == unique_dates[1]
            temp_df = df[is_date]
            count_old = temp_df['text'].str.contains(word).sum()
        except:
            pass 

        print(count)
        print(count_old)
        count_no.append(int(count))
        counter_old.append(count_old/len(df)*100)
        counter.append(count/len(df)*100)
        
        if(count_old != 0):
            percentage_change = (count-count_old)/count_old*100
        else:
            percentage_change = 0
        percentage_changer.append(percentage_change)
    insta = pd.read_csv('raw_dataset/cleaned_instagram.csv')
    total_insta_percent,insta_count = Percentage.percentage(word, insta, 'text')
    count_no.append(int(insta_count))
    insta_percent=line_graph(word,'raw_dataset/cleaned_instagram.csv','text')
    n=len(insta_percent)
    insta_percentage_latest=list(insta_percent[n-1].items())
    insta_percentage_2nd_last=list(insta_percent[n-2].items())
    percentage_change=(insta_percentage_latest[1][1]-insta_percentage_2nd_last[1][1])/insta_percentage_2nd_last[1][1]*100
    percentage_changer.append(percentage_change)
    counter.append(total_insta_percent)

     
    return counter,percentage_changer,count_no



def line_graph(word,path,attr):       
        
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')  # Convert date to Timestamp to group by week
    df = df[~(df['date'] < '2018-12-31')]  # Drop data before year 2019
    
    grouped_data = df[df[attr].str.contains(word, case=False, na=False)].groupby(df['date'].dt.floor('7D')).size().reset_index(name='count')
    
    # Change date to "mm-YYYY" format
    for i, row in grouped_data.iterrows():
        grouped_data.loc[i, 'date'] = str(grouped_data.loc[i, 'date'].week) + "-" + str(grouped_data.loc[i, 'date'].year)
    
    return grouped_data.to_dict(orient='record')



def getData(word):
    word=word.lower()
    word=stemming.stemming([word])[0]
    line_receipe=line_graph(word,paths[2],'text')
    line_packagedfoods=line_graph(word,paths[1],'text')
    line_menulinks=line_graph(word,paths[0],'text')
    line_instagram=line_graph(word,'raw_dataset/cleaned_instagram.csv','text')
    response = {
        "word_counter": word_count(word),
        "line_receipe": line_receipe,
        "line_packagedfoods": line_packagedfoods,
        "line_menulinks":line_menulinks,
        "line_instagram":line_instagram
    }
    return response

