from typing import Mapping
from urllib import parse
import scrapy
import pandas as pd
import csv
from datetime import date


class food_receipes(scrapy.Spider):

    name="food_receipes"
    start_urls = [
        'https://www.allrecipes.com/recipes/227/world-cuisine/asian/'
    ]
    receipes_countries=['chinese/','japanese/','korean/','indian/','pakistani/',
        'bangladeshi/','filipino/','indonesian/','malaysian/','thai/','vietnamese/']
    def parse(self, response):
        for countries in self.receipes_countries:
            self.start_urls = 'https://www.allrecipes.com/recipes/227/world-cuisine/asian/' + countries
            dish_links = response.xpath("//a[@class='carouselNav__link recipeCarousel__link']/@href").extract()
        
        for dish_link in dish_links:
            next_page  = dish_link
            yield scrapy.Request(next_page, callback=self.parseLinks)
    
    def parseLinks(self,response):
        links_to_dishes = response.xpath("//a[@class='card__titleLink manual-link-behavior']/@href").extract()
        links_to_dishes=list(dict.fromkeys(links_to_dishes))

        for food_link in links_to_dishes :
            next_page  = food_link
            yield scrapy.Request(next_page, callback=self.parseReceipes)

    def parseReceipes(self,response):
        dish_name = response.xpath("//h1[@class='headline heading-content']/text()").extract()
        ingredients = response.xpath("//span[@class='ingredients-item-name']/text()").extract()
        nutrition =   response.xpath("//span[@class='nutrient-name']/text()").extract()
        nutrition_daily_value = response.xpath("//span[@class='daily-value']/text()").extract()
        #do the preprocessing
        clean_ingredients,clean_nutrition=self.clean(ingredients,nutrition)
        today = date.today()

        if dish_name:

            yield {'date': today,'food name': dish_name , 'Ingredients' : clean_ingredients,
         'Nutrition' : clean_nutrition, 'nutrition value' : nutrition_daily_value }
    


    def clean(self,ingredients,nutrition):
        clean_ingredients = [item.replace('\t', "") for item in ingredients]
        clean_nutrition = [item.replace('\t', "") for item in nutrition]
        clean_nutrition = [item.replace('', "") for item in nutrition]
        clean_ingredients =[item.strip() for item in nutrition]
        clean_nutrition =[item.strip() for item in nutrition]


    

        return clean_ingredients,clean_nutrition
        
