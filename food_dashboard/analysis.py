from typing import Counter
import pandas as pd
import clean 
import os
import sys
import requests
sys.path.append('/home/sun/food_dashboard/food-dashboard-master')
import Percentage
import Interest_by_date
import Data
#paths
paths=['raw_dataset/cleaned_menu_links.csv','raw_dataset/cleaned_packaged_foods.csv','raw_dataset/cleaned_receipe.csv']
# paths=['raw_dataset/cleaned_receipe.csv']
def word_count(word):
    word=word.lower()
    word=clean.stemming([word])[0]
    print(word)

    counter =[]
    master_dict={}
    for path in paths:
        dict = {}
        file_name = path.split('/')[-1]
        df = pd.read_csv(path)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

        df['date'] = df['date'].apply(lambda x: "%d/%d" % (x.week, x.year))
        unique_dates=df['date'].unique()
        unique_dates[::-1].sort()
        count = 0
        count_old= 0
        
    

        is_date = df['date'] == unique_dates[0]
        temp_df = df[is_date]
        count = temp_df['food name'].str.contains(word).sum()
        try:
            is_date = df['date'] == unique_dates[1]
            temp_df = df[is_date]
            coun_old = temp_df['food name'].str.contains(word).sum()
        except:
            pass 

        print(count)
        counter.append(count/len(df)*100)
        if(count_old != 0):
            percentage_change = count-count_old/count_old*100
        else:
            percentage_change = 0
    insta = Data.get_data('food-dashboard-master/data/instagram.json')
    insta_percent = Percentage.percentage(word, insta, 'text')
    counter.append(insta_percent)

     
    return counter,percentage_change



def line_graph(word):       
        
    word=word.lower()
    word=clean.stemming([word])[0]
    counter =[]
    master_dict={}
    for path in paths:
        dict = {}
        file_name = path.split('/')[-1]
        df = pd.read_csv(path)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

        df['date'] = df['date'].apply(lambda x: "%d/%d" % (x.week, x.year))
        unique_dates=df['date'].unique()
        unique_dates[::-1].sort()
        count = 0
        count_old= 10

        for index, row in df.iterrows():

            for i in unique_dates:
                try:
                    if(row['date'] == i):    
                        if word in row['food name'].lower():
                            count += 1
                    dict[i] = count
                    count = 0
                except:
                    pass
    master_dict[file_name]=dict 
     
    return master_dict

print(word_count("Filipino"))
