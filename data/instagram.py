import pandas as pd

# df = pd.read_json(r'instagram.json')
# print(df.shape[0])
# df.to_csv (r'instagram.csv', index = None)

df = pd.read_csv('yelp.csv')
df.to_json('restaurant.json', orient='records')