import os
import cloudscraper
import re
from urllib.parse import urljoin, urlencode
import json
import time
import requests
import random
from bs4 import BeautifulSoup
from brands import Brand

URL = "https://www.vinted.fr/catalog"

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

def extract_csrf_token(text):
    match = re.search(r'"CSRF_TOKEN":"([^"]+)"', text)
    if match:
        return match.group(1)
    else:
        return None

def create_vinted_session():
    session = cloudscraper.create_scraper()
    session.headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',  # Ensure fresh data
        'Pragma': 'no-cache',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    req = session.get("https://www.vinted.nl/")
    csrfToken = extract_csrf_token(req.text)
    print(csrfToken)
    session.headers['X-CSRF-Token'] = csrfToken
    return session

def main():
    print("THE SCRIPT PROPERLY LAUNCHED")
    session = create_vinted_session()
    while True:        
        params = generate_params()
        print(params)
        full_url = urljoin(URL, '?' + urlencode(params))
        print(full_url)
        try:
            response = session.get(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            section = soup.find('section')
            children = len(section.find_all(recursive=False))
            print(section.find_all(recursive=False))
            print("Children = ", children)
            # print(items)
            time.sleep(5)
        except requests.exceptions.HTTPError as httperr:
            if httperr.response.status_code in [401, 403]:
                print(f"PAUSING DUE TO UNAUTHORIZED: {httperr}")
                # time.sleep(60)
            else: 
                print(f'A HTTP ERROR OCCURED: {httperr}"')
        except Exception as exp:
            print(f'AN ERROR OCCURED: {exp}"')

if __name__ == "__main__":
    main()