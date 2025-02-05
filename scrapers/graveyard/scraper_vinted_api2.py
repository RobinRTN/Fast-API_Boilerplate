import os
import cloudscraper
import re
from urllib.parse import urljoin, urlencode
import json
import time
import requests
import random
from brands import Brand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.1020.40 Safari/537.36 Edg/95.0.1020.40",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; CrOS x86_64 13904.77.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
]

HOSTS = ["fr", "nl", "de", "es"]

HOST_LANG = {"fr": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3", "nl": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7", "de": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7", "es": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7"}

def extract_csrf_token(text):
    match = re.search(r'"CSRF_TOKEN":"([^"]+)"', text)
    if match:
        return match.group(1)
    else:
        return None

def generate_params():
    brand_ids = [brand.value for brand in Brand]
    params = [
        ("time", int(time.time())),
        ("catalog_from", 0),
        ("page", 1),
        ("order", "newest_first"),
        ("catalog[]", 2050)
    ]
    params.extend(("brand_ids[]", brand_id) for brand_id in brand_ids)
    return params

def setup_browser(user_agent):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("window-size=1280,800")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    return driver

def anti_bot(raw_data, driver, url):
    counter = 0
    while "Verifying you are human." in raw_data:
        print("Bot detected, pausing and retrying it")
        time.sleep(random.randint(3, 5))
        driver.get(url)
        time.sleep(random.randint(2,3))
        raw_data = driver.find_element(By.TAG_NAME, 'body').text
        counter += 1
        if counter == 4:
            break

def process_data(raw_data, hash_map):
    try:
        parsed_data = json.loads(raw_data)
        if "items" in parsed_data:
            current_time = datetime.now()
            for item in parsed_data["items"]:
                print(item["title"])
                id = item["id"]
                if id not in hash_map:
                    print("NEW ITEM !")
                    hash_map[id] = current_time
            print("All scraped properly, well done")
        else:
            print("No items found in data.")
    except json.JSONDecodeError:
        print("Failed to decode JSON.")

def verify_cookies(driver):
    cookies = driver.get_cookies()
    for cookie in cookies:
        print(cookie)
        print("====")

def setup_fetching_elements(agent):
    params = generate_params()
    url = "https://www.vinted.nl/api/v2/catalog/items"
    full_url = urljoin(url, '?' + urlencode(params))
    print("params =>", params)
    print("url => ", full_url)
    return (full_url)

def fetch_data(agent, hash_map):
    full_url = setup_fetching_elements(agent)
    try:
        driver = setup_browser(agent)
        driver.get("https://www.vinted.nl/")
        verify_cookies(driver)
        time.sleep(random.randint(2,3))
        actions = ActionChains(driver)
        actions.move_by_offset(random.randint(0, 50), random.randint(0, 50))
        actions.perform()
        driver.get(full_url)
        time.sleep(random.randint(2,3))
        raw_data = driver.find_element(By.TAG_NAME, 'body').text
        anti_bot(raw_data, driver, full_url)
        process_data(raw_data, hash_map)
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
    finally: 
        driver.quit()

def randomised_host_agents():
    host = 'nl'
    agent = USER_AGENT[random.randint(0, 7)]
    url = f"https://www.vinted.{host}/api/v2/catalog/items"
    return (host, agent, url)

def should_rotate(rotation_counter):
    rotation_counter += 1
    if rotation_counter >= random.randint(15, 18):
        rotation_counter = 0
        return True
    else:
        return False

def rotate_agent():
    agent = USER_AGENT[random.randint(0, 7)]
    return (agent)


def main():
    rotation_counter = 0
    agent = rotate_agent()
    hash_map = {}
    while True:
        if should_rotate(rotation_counter):
            agent = rotate_agent()
        try:
            fetch_data(agent, hash_map)
            rand_time = random.randint(5, 14)
            print(f"Waiting for {rand_time} seconds before next one ...")
            time.sleep(rand_time)
        except requests.exceptions.HTTPError as httperr:
            if httperr.response.status_code in [401, 403, 100]:
                print(f"Pausing 60 seconds to avoid unauthorized ...: {httperr}")
            else: 
                print(f'A http error occured: {httperr}"')
            time.sleep(60)
        except Exception as exp:
            print(f'An error occured: {exp}"') 
            time.sleep(60)

if __name__ == "__main__":
    main()