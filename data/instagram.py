import pandas as pd

df = pd.read_json(r'instagram_new.json')
df2=pd.read_csv(r'instagram.csv')
# print(df.shape[0])
df.to_csv (r'instagram_new.csv', index = None)
df.append(df2)

# df = pd.read_csv('yelp.csv')
# df.to_json('restaurant.json', orient='records')