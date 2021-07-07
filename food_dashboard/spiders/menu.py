from typing import Mapping
from urllib import parse
import scrapy
import pandas as pd
from datetime import date
import re
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
        today = date.today()
        
        for name in raw_food_name:
             #do the preprocessing
            clean_name=self.clean(name)
            if clean_name:
                yield {'date': today,'food name': clean_name}

    def clean(self,name:str):
        # n in names
        name=name.replace('\t','')
        name= re.sub("([^\x00-\x7F])+","",name)
 
        return name
        


