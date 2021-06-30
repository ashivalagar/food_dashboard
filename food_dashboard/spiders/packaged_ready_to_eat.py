from typing import Mapping
from urllib import parse
import scrapy
import pandas as pd
import csv
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from datetime import date



class food_menu(scrapy.Spider):

    name="packaged_food_ready_to_eat"
    start_urls = [
        'https://www.fairprice.com.sg/category/ready-to-eat--1?filter=Country%20Of%20Origin%3AChina%2CHong%20Kong%2CIndia%2CJapan%2CMalaysia%2CSingapore'
    ]
    def __init__(self):
        self.driver =self.__get_driver()

    def parse(self, response):
        for i in range(1,40):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
        time.sleep(3)  
        sel = Selector(text=self.driver.page_source)    
        packaged_links = sel.xpath("//a[@class='sc-1plwklf-3 bmUXOR']/@href").extract()
        
        for packaged_link in packaged_links:
            next_page  = 'https://www.fairprice.com.sg' + packaged_link
            yield scrapy.Request(next_page, callback=self.parseLinks)

    def parseLinks(self,response):
        packaged_food_name = response.xpath("//span[@class='sc-1bsd7ul-1 djlKtC']/text()").extract()
        ingredients = response.xpath("//ul[@class='sc-3zvnd-2 gersHj']/li/span/text()").extract()
        nutrition_info = response.xpath("//li[@class='sc-3zvnd-6 iyTtYO']/div/text()").extract()
        today = date.today()

        yield {'date': today, 'packaged food name': packaged_food_name , 'Ingredients' : ingredients,
        'Nutrition' : nutrition_info }

    def __get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome('/home/sun/food_dashboard/food_dashboard/chromedriver')
        driver.get('https://www.fairprice.com.sg/category/ready-to-eat--1?filter=Country%20Of%20Origin%3AChina%2CHong%20Kong%2CIndia%2CJapan%2CMalaysia%2CSingapore')
        

        return driver
        


