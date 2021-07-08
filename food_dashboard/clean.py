from os import setegid
from nltk import stem
from nltk.stem import PorterStemmer
import math
import re
import pandas as pd
import csv


#create an object of class PorterStemmer
porter = PorterStemmer()
paths= ['/home/sun/food_dashboard/raw_dataset/menu_links.csv','/home/sun/food_dashboard/raw_dataset/packaged_foods.csv','/home/sun/food_dashboard/raw_dataset/receipe.csv']
new_paths=['/home/sun/food_dashboard/raw_dataset/cleaned_menu_links.csv','/home/sun/food_dashboard/raw_dataset/cleaned_packaged_foods.csv','/home/sun/food_dashboard/raw_dataset/cleaned_receipe.csv','/home/sun/food_dashboard/raw_dataset/cleaned_instagram.csv']


def stemming(sentences):
    stemmed_sentences=[]
    for sentence in sentences:
        new_sentence = []
        for word in sentence.split():
                new_sentence.append(porter.stem(word))
        new_sentence = ' '.join(new_sentence)
        stemmed_sentences.append(new_sentence)
    return stemmed_sentences

i = 0
for path in paths :
    data = pd.read_csv(paths[i])
    nan_value = float("NaN")
    data.replace("", nan_value, inplace=True) 
    data.dropna(subset = ["food name"], inplace=True)
    data["food name"] = stemming(data["food name"])  
    data.to_csv(new_paths[i] ,index=False)
i+=1

data = pd.read_csv('food-dashboard-master/data/instagram.csv')
nan_value = float("NaN")
data.replace("", nan_value, inplace=True) 
data.dropna(subset = ["text"], inplace=True)
data['text']=stemming(data["text"])
data.to_csv(new_paths[3] ,index=False)





# def non_english_words(sentences):
#     stemmed_sentences=[]
#     for sentence in sentences:
#         name= re.sub("([^\x00-\x7F])+","",sentence)
#         return name

# def tab_space(sentences):




    

            
             

