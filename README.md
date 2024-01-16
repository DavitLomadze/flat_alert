# README for Flat Listing Scraper Bot
## Introduction
This Python script is designed for web scraping flat listings from a specified real estate website and automatically updating a local CSV file with new listings. Additionally, it sends notifications about these new listings to a specified Telegram chat.

## Features
- Scrapes data from a real estate website.
- Updates a local CSV file with new listings.
- Sends notifications via Telegram for new listings.

## Requirements
- Python
- Libraries: BeautifulSoup, requests, pandas, telegram, os, asyncio, time

## Setup
**Install Dependencies**: Install the required Python libraries using pip install beautifulsoup4 requests pandas python-telegram-bot.

**Telegram Bot**: Create a Telegram bot and get the token. Set the TOKEN variable in the script with your bot's token. Also, set your Telegram chat ID in CHAT_ID.

**CSV File Directory**: The script uses a CSV file (flat_listing.csv) to store and update the listings. Make sure to have this file in the script's directory or update the CSV_DIR variable accordingly.

## Usage
**Run the Script**: Execute the script. It will scrape the website, update the CSV file, and send Telegram messages for new listings.

## Function Descriptions
- change_dir(): Changes the current working directory.
- read_flat_listing(): Reads the existing flat listings from the CSV file.
- request_html(): Requests the HTML content from the source URL.
- parse_to_html(response): Parses the HTML response using BeautifulSoup.
- scrapped_df(soup): Extracts flat listings data and returns it as a DataFrame.
- send_message(token, chat_id, text): Sends a message to the specified Telegram chat.
- main(): The main function that orchestrates web scraping, updating the CSV file, and sending Telegram notifications.

## Security Note
Keep your Telegram bot token secure and do not share it publicly.

## Disclaimer
**Web scraping can be against the terms of service of some websites. Ensure you have permission to scrape data from the website.**

## Contribution
Feel free to contribute to this project by suggesting improvements or submitting pull requests.
