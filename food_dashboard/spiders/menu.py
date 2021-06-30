from typing import Mapping
from urllib import parse
import scrapy
import pandas as pd
import csv
from ..clean import stemming


class food_menu(scrapy.Spider):

    name="food_menu"
    start_urls = [
        'https://www.foodline.sg/tingkat/?PostalCode=&StartDate=&PackageLength=1-100&Pax=&PropertyType=HDB'
    ]
    
    def parse(self, response):
        menu_links = response.xpath("//div[@class='searchResultMenuTbl']/a/@href").extract()
        # yield {'href': menu_card}
        # with open('raw_dataset/menu_links.csv') as csvfile:
            # menu_links = list(csv.reader(csvfile))
        
        for menu_link in menu_links:
            next_page  = 'https://www.foodline.sg/'+menu_link
            yield scrapy.Request(next_page, callback=self.parseMenu)
    
    def parseMenu(self,response):
        raw_food_name = response.xpath("//table[@class='menuWeeklyTbl']/tr[position()>1]/td[position()>2]/text()").extract()
        
        for name in raw_food_name:
            #do the preprocessing
            clean_name=self.clean(name)
            clean_name1 = stemming(clean_name1)
            yield {'food name': clean_name}

    def clean(self,name:str):
        # n in names
        name=name.replace('\t','')
        # if(not isasccii()):
        #     name=name.replace()

        return name
        


