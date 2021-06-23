from typing import Mapping
from urllib import parse
import scrapy
import pandas as pd
import csv


class food_receipes(scrapy.Spider):

    name="food_receipes"
    start_urls = [
        'https://www.allrecipes.com/recipes/227/world-cuisine/asian/'
    ]
    receipes_countries=['chinese/','japanese/','korean/','indian/','pakistani/','bangladeshi/','filipino/','indonesian/','malaysian/','thai/','vietnamese/']
    def parse(self, response):
        for countries in self.receipes_countries:
            self.start_urls = 'https://www.allrecipes.com/recipes/227/world-cuisine/asian/' + countries
            dish_links = response.xpath("//a[@class='carouselNav__link recipeCarousel__link']/@href").extract()
        
        for dish_link in dish_links:
            next_page  = dish_link
            yield scrapy.Request(next_page, callback=self.parseMenu)
    
    def parseReceipe(self,response):
        links_to_dishes = response.xpath("//a[@class='card__titleLink manual-link-behavior']/@href").extract()
        links_to_dishes=list(dict.fromkeys(links_to_dishes))
        for name in links_to_dishes :
            

            #do the preprocessing
            clean_name=self.clean(name)
            yield {'Food name': clean_name}

    def clean(self,name:str):
        name=name.replace('\t','')
        # if(not isasccii()):
        #     name=name.replace()

        return name
        
