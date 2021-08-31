# Food-scraping


## How to run food scraping for 
1) Food name in menu from foodline.sg
2) Food name, Ingredients list and Nutrition value for Receipes from allreceipes.com
3) Food name,Ingredients list and Nutrition info for packaged foods from fairprice.com

Setup:
    1)Install chromedriver for your OS(windows,mac,linux)
    2)pip3 install -r requirements.txt
## Scraping Menu

1) go to food_dashboard/settings.py uncomment line no. 16 (uncommenting can be done by removing the #) save the settings.py file.

2) open terminal and make sure you are in FOOD_DASHBOARD folder now type this "scrapy crawl food_menu" and press enter. wait until it has completely run once it has run go to raw_dataset/menu_links.csv and see if at the below the latest date has been added 
    
## Scraping Receipes
1) go to food_dashboard/settings.py comment out line no. 16 (commenting can be done by adding the #) uncomment line no. 17 (uncommenting can be done by removing the #) save the settings.py file

2) open terminal and make sure you are in FOOD_DASHBOARD folder now type this "scrapy crawl food_receipes" and press enter. wait until it has completely run once it has run go to raw_dataset/receipe.csv and see if at the below the latest date has been added 

## Scraping Instagram  
1) Open jupyter notebook named Instagram.ipynb
2) Run all cells in the order 


## final 
1) cd food_dashboard 
2) python3 clean.py


 
