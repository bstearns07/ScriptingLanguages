import time

import requests
from bs4 import BeautifulSoup
urls = [
'https://www.bbc.com/news',
'https://www.allrecipes.com',
'https://www.Kaggle.com/datasets'
]

def scrape_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = soup.find_all('title') # Change this to target other elements as needed
        return [title.get_text() for title in titles]
    else:
        print(f"Failed to retrieve {url} with status code {response.status_code}")
        return []

all_data = []
for url in urls:
    data = scrape_data(url)
    all_data.extend(data)
    time.sleep(3)
    for item in all_data:
        print(item)
