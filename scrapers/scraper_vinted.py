from urllib.parse import urljoin, urlencode
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from brands import Brand
import time
import random
import json
import requests

AUTH = 'brd-customer-hl_0cf02a30-zone-scraping_browser1-session-{session_id}:35x09a0e3b3v'
SBR_WEBDRIVER_TEMPLATE = 'https://{auth}@brd.superproxy.io:9515'

def send_data_to_backend(fresh_items):
    print("Sending the fresh items to backend ...")
    try:
        url = "http://backend:5000/api/items/fresh_items"
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=fresh_items, headers=headers)
        if response.status_code == 200:
            print("Data sent successfully")
            response_json = response.json()
            print("Server response to scraper: ", response_json.get("msg"))
        else:
            print(f"Failed to send fresh item data to the backend: {response.status_code}")

    except Exception as e:
        print("Issue when sending the data: ",  e)

def get_url():
    url = "https://www.vinted.fr/api/v2/catalog/items"
    brand_ids = [brand.value for brand in Brand]
    params = [
        ("time", int(time.time())),
        ("catalog_from", 0),
        ("page", 1),
        ("order", "newest_first"),
        ("catalog[]", 2050)
    ]
    params.extend(("brand_ids[]", brand_id) for brand_id in brand_ids)
    full_url = urljoin(url, "?" + urlencode(params))
    return full_url

def extract_data(parsed_data, hash_map):
    try:
        fresh_items = []
        current_time = datetime.now()
        for item in parsed_data["items"]:
            id = item["id"]
            if id not in hash_map:
                fresh_items.append(item)
                hash_map[id] = current_time
        print(f"{len(fresh_items)} new items in request")
        send_data_to_backend(fresh_items)
    except Exception as e:
        print("Issue with the parsing", e)

def hash_map_clean(hash_map):
    counter = 0
    current_time = datetime.now()
    keys_to_remove = []

    for key, value in hash_map.items():
        if current_time - value > timedelta(minutes=4):
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del hash_map[key]
        counter += 1

    print(f"Cleaned up {counter} elements in hashmap")

def fetch_data_process(url, hash_map):
    """
    Connects to Bright Data's Scraping Browser and performs scraping tasks.
    """
    try:
        session_id = random.randint(1, 10_000)
        auth = AUTH.format(session_id=session_id)
        sbr_connection_url = SBR_WEBDRIVER_TEMPLATE.format(auth=auth)
        print(f"Connecting to Scraping Browser with session ID: {session_id}...")

        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        sbr_connection = ChromiumRemoteConnection(sbr_connection_url, 'goog', 'chrome')
        with Remote(sbr_connection, options=options) as driver:
            print('Connected! Navigating to the main page...')
            
            driver.get('https://www.vinted.fr/')
            print('Landing page loaded successfully.')

            for i in range(7):
                print(f'Performing API request {i + 1}...')
                driver.get(url)
                
                raw_data = driver.find_element(By.TAG_NAME, 'body').text
                print(f"Successful API call for request {i + 1}")
                parsed_data = json.loads(raw_data)
                
                if "items" in parsed_data:
                    extract_data(parsed_data, hash_map)
                else:
                    print("Bot detected, rotating the proxy prematurely...")
                    break
                wait_time = random.randint(3, 6)
                print(f'Waiting {wait_time} seconds before next request...')
                time.sleep(wait_time)
            
            print('All API requests completed successfully for this session.')

    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    hash_map = {}
    url = get_url()
    iteration = 1
    while True:
        print(f'\nStarting scraping session {iteration}...\n')
        fetch_data_process(url, hash_map)
        print(f'\nScraping session {iteration} completed.\n')
        time.sleep(random.randint(2, 3))
        iteration += 1
        hash_map_clean(hash_map)


if __name__ == '__main__':
    main()