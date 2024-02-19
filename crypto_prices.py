# Scraping To #CoinDesk# WebSite From Page #CryptoPrices

# Created by Abdullah EL-Yamany


# Note => An error can occur if the site has been modified
#      => After running the code, you can go to the csv file.  to see the results

# ===============================

import requests as rq
from bs4 import BeautifulSoup as bs
import csv
from itertools import zip_longest

page_url = "https://www.coindesk.com/tag/news/"


list_article_name = []
list_authors = []


def get_page_data(page_url, page_number):
    
    page = rq.get(f"{page_url}/{page_number}/")
    src = page.content    # == page.text
    soup = bs(src, 'lxml')



    # Get article names
    article_names = soup.find_all("a", {'class': 'card-title'})
    
    remove_article_string = [ "Crypto News Roundup"]

    for name in article_names :
        
        if any(remove_str in name.text for remove_str in remove_article_string) or name.text == "": 
            continue

        list_article_name.append(name.text)
        
    # Get author names
    authors_names = soup.find_all("span", {'class': 'typography__StyledTypography-sc-owin6q-0 hirYAs'})

    remove_author_string= ["", "Sponsored", "Subscribe", "Upcoming Events", "See All Newsletters"]
    
    for name in authors_names :
        if (name.text in remove_author_string ) :
            continue

        list_authors.append(name.text)



    file_list = [list_article_name, list_authors]

    exported = zip_longest(*file_list)


    with open('coindesk-data.csv', 'a') as csv_file :

        writer = csv.writer(csv_file)
        # writer.writerow(["Coin Name", "abbreviation", "Price in relation to the dollar", "The rate high or low in last 24 hours"])
        if page_number == 1: 
            writer.writerow(["Article Name", "Authors"])
        writer.writerows(exported)
        print("All Done!")



for i in range(1, 10):
    get_page_data(page_url, i)
