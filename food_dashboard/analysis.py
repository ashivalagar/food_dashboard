from typing import Counter
import pandas as pd
from clean import stemming
#paths
paths= ['/home/sun/food_dashboard/raw_dataset/menu_links.csv','/home/sun/food_dashboard/raw_dataset/packaged_foods.csv','../raw_dataset/receipe.csv']

def word_count(word):
    word = word.lower()
    word=stemming([word])[0]
    counter =[]
    for path in paths:
        data = pd.read_csv(path)
        count = 0
        for sentence in data['food name']:
            if word in sentence.lower():
                count += 1
        counter.append(count/len(data)*100)
    return counter

print(word_count("2-minute instant noodle"))
        
        

