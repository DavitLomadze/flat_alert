from bs4 import BeautifulSoup
import requests
import pandas as pd
import telegram
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
import asyncio
import time

# Change directory
def change_dir():
    os.chdir('D:\\automation\\flat listing')

# Telegram bot token and chat id (Keep these secret)
TOKEN = "HIDDEN"
CHAT_ID = "HIDDEN"

# Source URL
SOURCE_URL = "https://www.myhome.ge/ka/search/?UserID=3336951"

# CSV file directory
CSV_DIR = './flat_listing.csv'

FILENAME = 'flat_listing.csv'

# Identify as a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Read CSV file
def read_flat_listing():
    df = pd.read_csv(CSV_DIR)
    return df

# Request HTML codes
def request_html():
    response = requests.get(SOURCE_URL, headers=headers)
    return response

# Parse HTML content using BeautifulSoup
def parse_to_html(response):
    
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# consolidate scrapped data
def scrapped_df(soup):
    
    # get list of flats
    spans_with_id = [span.text.strip() for span in soup.find_all('span') if span.get('class') == ['d-block']] # id
    hrefs_of_card_containers = [a_tag.get('href').strip() for a_tag in soup.find_all('a', class_='card-container')] # href
    address_elements = [div.text.strip() for div in soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['address'])]
    price_elements = [b_tag.text.strip() for b_tag in soup.find_all(lambda tag: tag.name == 'b' and tag.get('class') == ['item-price-usd', 'mr-2'])]
    details_elements = [div.text.strip() for div in soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['d-flex', 'options'])]
    kv_elements = [div.text.strip() for div in soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['item-size'])]
    date_elements = [span.text.strip() for span in soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['d-block', 'mb-3'])]
    
    rent_listing = pd.DataFrame(data={'id': spans_with_id, 
                                  'link': hrefs_of_card_containers, 
                                  'address': address_elements, 
                                  'price': price_elements, 
                                  'details': details_elements, 
                                  'kv': kv_elements, 
                                  'date': date_elements})
    
    return rent_listing
    

async def send_message(token, chat_id, text):
    bot = telegram.Bot(token)
    try:
        await bot.send_message(chat_id, text)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.close()

async def main():
    
    # web scrapping
    response = request_html()
    
    if response.status_code == 200:
    
        # parse to bs4
        soup = parse_to_html(response)
    
        # scrapp into a dataframe
        new_listing = scrapped_df(soup)   

        # get from saved list
        change_dir()
        listed_df = read_flat_listing()
        
        # get latest id
        latest_id = listed_df.id.str.strip('ID ').astype('int').max()
        
        # remove old ids
        new_listing = new_listing[lambda row: row.id.str.strip('ID ').astype('int') > latest_id]
        
        # update list, by concating new listings
        listed_df = pd.concat([listed_df, new_listing])
        listed_df.to_csv(FILENAME, index=False)
        
        # send message
        if new_listing.shape[0] != 0:
            for id in range(new_listing.shape[0]):
                await send_message(TOKEN, CHAT_ID, new_listing.loc[id].to_string())
                time.sleep(1)
                                
        else:
            print('no new ids')
        
    else:
        print(f'bad response: {response.status_code}')
        


if __name__ == "__main__":
    asyncio.run(main())


