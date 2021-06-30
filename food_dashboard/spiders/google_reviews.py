from typing import Mapping
from urllib import parse
import scrapy
import pandas as pd
import csv


class food_menu(scrapy.Spider):

    name="food_menu"
    start_urls = [
        'https://www.theworlds50best.com/asia/en/list/1-50'
    ]
    
    def parse(self, response):
        restaurant_links = response.xpath("//a[@class='item ']/h2/text()").extract()
        # yield {'href': menu_card}
        # with open('raw_dataset/menu_links.csv') as csvfile:
            # menu_links = list(csv.reader(csvfile))
        
        for restaurant_link in restaurant_links:
            # next_page  = 
            # yield scrapy.Request(next_page, callback=self.parseMenu)
            return