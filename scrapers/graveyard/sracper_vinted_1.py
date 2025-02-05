import os
import cloudscraper
import re
from urllib.parse import urljoin, urlencode
import json
import time
import requests
import random
from brands import Brand

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

def create_vinted_session(host, user_agent):
    print("HOST = ", host)
    session = cloudscraper.create_scraper()
    session.headers = {
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en',
        'Cache-Control': 'no-cache',  # Ensure fresh data
        'Pragma': 'no-cache',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    req = session.get(f"https://www.vinted.{host}/")
    csrfToken = extract_csrf_token(req.text)
    print(csrfToken)
    session.headers['X-CSRF-Token'] = csrfToken
    return session

def main():
    print("THE SCRIPT PROPERLY LAUNCHED")
    loops = 0
    id_set = set()
    while True:
        hosts = ["fr", "nl", "de", "es"]
        host = hosts[loops % 4]
        user_agent = USER_AGENT[(loops + random.randint(0, 4)) % 8]
        top_range = random.randint(6, 14)
        for element in range(0, top_range):        
            session = create_vinted_session(host, user_agent)
            params = generate_params()
            print(params)
            url = f"https://www.vinted.{host}/api/v2/catalog/items"
            full_url = urljoin(url, '?' + urlencode(params))
            print(full_url)
            pause = random.randint(4, 12)
            try:
                response = session.get(full_url)
                if response.status_code != 403:
                    data = response.json()
                    print("Length = ", len(data['items']))
                    for item in data["items"]:
                        id = int(item["id"])
                        print("id = ", id)
                        if id not in id_set:
                            id_set.add(id)
                            print("Item title => ", item["title"])
                    print("Data retrieved successfully")
                    time.sleep(pause)
                    print(f"Waited for {pause} seconds...")
                else:
                    print("PAUSING BECAUSE OF ", response.status_code)              
                    time.sleep(pause)
                
            except requests.exceptions.HTTPError as httperr:
                if httperr.response.status_code in [401, 403, 100]:
                    print(f"PAUSING DUE TO UNAUTHORIZED: {httperr}")
                    time.sleep(60)
                else: 
                    print(f'A HTTP ERROR OCCURED: {httperr}"')
            except Exception as exp:
                print(f'AN ERROR OCCURED: {exp}"')
            loops += 1

if __name__ == "__main__":
    main()