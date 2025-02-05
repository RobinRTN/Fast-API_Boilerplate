from urllib.parse import urljoin, urlencode
import time
import requests
import random
from bs4 import BeautifulSoup
from brands import Brand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

URL = "https://www.vinted.fr/catalog"

def setup_browser():
    options = Options()
    options.add_argument("--headleass")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path="~goinfre/chromedriver")
    driver = webdriver.Chrome(options=options)
    return driver
    

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

def main():
    params = generate_params()
    print(params)
    full_url = urljoin(URL, '?' + urlencode(params))
    print(full_url)
    driver = setup_browser()
    while True:        
        try:
            driver.get(full_url)
            time.sleep(5)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            section = soup.find('section')
            # children = len(section.find_all(recursive=False))
            # print(section.find_all(recursive=False))
            items = section.find_all('div', class_="new-item-box__container")
            for item in items: 
                print('====')
                print(item)
                print('====')
            # print("Children = ", children)
        except requests.exceptions.HTTPError as httperr:
            if httperr.response.status_code in [401, 403]:
                print(f"PAUSING DUE TO UNAUTHORIZED: {httperr}")
                time.sleep(60)
            else: 
                print(f'A HTTP ERROR OCCURED: {httperr}"')
        except Exception as exp:
            print(f'AN ERROR OCCURED: {exp}"')

if __name__ == "__main__":
    main()