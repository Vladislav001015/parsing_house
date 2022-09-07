import decimal
import multiprocessing
from datetime import datetime

from models import House
from settings_db import db
from bs4 import BeautifulSoup as BS
from utils import get_html


# BASE_URL = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'

def get_houses(soup: BS):
    """
    function to search for all required fields on the site
    """
    all_houses = soup.find_all('div', class_="clearfix") # get main block with all house on one page
    
    for house in all_houses[1:]:
        
        try:
            house_img = house.find('picture').find('img').get('data-src') # getting a house image
        except AttributeError:
            house_img = ''
        
        try:
            house_title = house.find('div', class_='title').text.strip() # getting a house title
        except AttributeError:
            house_title = ''
        
        try:
            house_location = house.find('div', class_='location').find('span', class_='').text.strip() # getting a house location
        except AttributeError:
            house_location = ''
        
        try:
            house_date = house.find('div', class_='location').find('span', class_='date-posted').text.strip('<').strip() # getting a house posted date
            house_date = datetime.strptime(house_date, "%d/%m/%Y")
        except (AttributeError, ValueError):
            house_date = datetime.now().strftime("%d-%m-%Y")
            
        try:
            house_desc = house.find('div', class_='description').text.strip().split('\n')[0] # getting a house description
        except AttributeError:
            house_desc = ''

        try:
            
            house_price = house.find('div', class_='price').get_text().strip() # getting a house price
            if '$' in house_price: # check currency, just many houses have text instead of a price
                try:
                    house_price = decimal.Decimal(house_price.replace(',', '.')[1:].replace('.',''))
                    house_currency = 'USD'
                except decimal.InvalidOperation: # if two prices are indicated, I leave the first price
                    house_price = house_price.split('\n')[0]
                    house_price = decimal.Decimal(house_price.replace(',', '.')[1:].replace('.',''))
                    house_currency = 'USD'
            else:
                house_currency = house_price
                house_price = 0
                
        except AttributeError:
            house_price = 0
            house_currency = ''

        try:
            house_bedroom = house.find('span', class_='bedrooms').get_text().strip().replace(' ', '').replace('\n', '') # count of bedroom in house
        except AttributeError:
            house_bedroom = ''
        
        data = { 
            'title': house_title,
            'description': house_desc,
            'location': house_location,
            'price': house_price,
            'bedroom': house_bedroom,
            'posted_at': house_date,
            'currency': house_currency,
            'image': house_img
        } # preparing data for loading
        add_house_to_db(data)

def multiprossing_parse(l, url):
    l.acquire()
    try:
        get_houses(BS(get_html(url), 'lxml'))
    finally:
        l.release()

def add_house_to_db(data):
    # db.connect()
    house = House(**data)
    house.save()
    

# def check_end_page(soup: BS): # need to finish
#     page = soup.find('div', class_='pagination').find('span', class_='selected').text
#     return page



def parse():
    LAST_PAGE = 94 + 1 # range does not go through the last number
    lock = multiprocessing.Lock()
    for i in range(1, LAST_PAGE):
        url = f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i}/c37l1700273'

        # multiprocessing.Process(target=multiprossing_parse, args=(lock, url)).start() # started multiprocessing (need to finish)
        get_houses(BS(get_html(url), 'lxml')) # normal way to start, 
        print(f'Парсинг {i} страницы завершен!')