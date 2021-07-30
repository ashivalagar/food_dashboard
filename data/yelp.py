import pandas as pd
import numpy as np
import json
import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
%matplotlib inline

#Need to use a delay between page scrapes in order to limit getting blocked by Yelp
from time import sleep

#ENTER SEARCH TERMS BELOW:
cuisine_type = "Italian"
location = "Albany, NY"

#Generate URL based on search terms
base_url = "https://www.yelp.com"
search_url = f"{base_url}/search?find_desc={cuisine_type}&find_loc={location}"

#Or manually set search_url by copying directly from Yelp Page if desired
#search_url = "https://www.yelp.com/search?find_desc=burger&find_loc=Albany%2C%20NY"

star_container_class = "lemon--div__373c0__1mboc attribute__373c0__1hPI_ display--inline-block__373c0__2de_K u-space-r1 border-color--default__373c0__2oFDT"
price_range_class = "lemon--span__373c0__3997G text__373c0__2pB8f priceRange__373c0__2DY87 text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-bullet--after__373c0__1ZHaA"
review_count_class = "lemon--span__373c0__3997G text__373c0__2pB8f reviewCount__373c0__2r4xT text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_"
next_page_class = "lemon--a__373c0__IEZFH link__373c0__29943 next-link navigation-button__373c0__1D3Ug link-color--blue-dark__373c0__1mhJo link-size--default__373c0__1skgq"
search_result_class = "lemon--div__373c0__1mboc searchResult__373c0__1yggB border-color--default__373c0__2oFDT"

next_page_url = search_url
page_counter = 1
business_list = []

#Run continuously until there is no longer a "next page" url found.
while next_page_url:
    #Request HTML page and load into Beautiful Soup object
    request = requests.get(next_page_url)
    soup = BeautifulSoup(request.content,'html.parser')
    
    #Find search results container on page.
    search_results = soup.findAll(class_=search_result_class)
    print(f"Page {page_counter}, {len(search_results)-1} results {next_page_url}")
    result_counter = 1
    
    #Loop through search results and store information for each business
    for search_result in search_results:
        business_info = {}
        try:
            business_name_url = search_result.findAll('a', href=True)[1]
            business_info['url'] = f"https://www.yelp.com{business_name_url['href']}"
            business_info['name'] = business_name_url['name']
            business_info['biz_id'] = business_name_url['href'].split('/biz/')[1].split('?')[0]
        except:
            continue
            
        try:
            business_info['address'] = search_result.find('address').text
        except:
            pass
        try:
            business_info['category'] = [category.text for category in search_result.findAll("a",attrs={"role":"link"})]
        except:
            pass
        try:
            business_info['star_rating'] = float(re.findall(r"[-+]?\d*\.\d+|\d+", 
                                                      search_result.find(
                                                          class_=star_container_class).find('div')['aria-label'] )[0] )
        except:
            pass
        try:
            business_info['price_range'] = search_result.find(class_=price_range_class).text
        except:
            pass
        try:
            business_info['num_reviews'] = int(re.findall(r"[-+]?\d*\.\d+|\d+",
                                                      search_result.find(
                                                          class_=review_count_class).text )[0] )
        except:
            pass
        try:
            business_info['image_shown'] = search_result.find('img')['src']
        except:
            pass
        
        #Append business information for each search result to a list containing all businesses.
        if business_info:
            business_list.append(business_info)
            
        result_counter+=1
    
    #Set url for next page. If not found, break out of loop.
    if soup.find(class_=next_page_class):
        next_page_url = base_url + soup.find(class_=next_page_class)['href']
        page_counter+=1
    else:
        break
    
    #Random delay between 2 and 20 seconds to prevent getting blocked
    sleep(np.random.randint(2,20))

print(len(business_list), "businesses scraped")

