import requests
from bs4 import BeautifulSoup

url = 'https://scraping-for-beginner.herokuapp.com/udemy'

respons = requests.get(url)

soup = BeautifulSoup(respons.text, 'html.parser')
print(soup)