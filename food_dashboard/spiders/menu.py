from typing import Mapping
import scrapy
import pandas as pd
import csv


class food_menu(scrapy.Spider):

    name="food_menu"
    start_urls = [
        'https://www.foodline.sg/tingkat/?PostalCode=&StartDate=&PackageLength=1-100&Pax=&PropertyType=HDB'
    ]
    
    def parse(self, response):
        menu_card = response.xpath("//div[@class='searchResultMenuTbl']/a/@href").extract()
        yield {'href': menu_card}
        with open('raw_dataset/menu_links.csv') as csvfile:
            menu_links = list(csv.reader(csvfile))
        
        for menu_link in menu_links:
            next_page  = 'https://www.foodline.sg/'+menu_link
    
    def parse2(self,response)
            


