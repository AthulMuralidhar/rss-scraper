from bs4 import BeautifulSoup
import requests
from pprint import pprint

URL = "http://www.nu.nl/rss/Algemeen"


page = requests.get(URL)
soup = BeautifulSoup(page.content, 'lxml')

# pprint(soup.find_all('item'))

for item in soup.find_all('item'):
    pprint(item)
    print()
    print()
    # break
