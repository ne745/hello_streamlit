from tkinter import W
import requests
from bs4 import BeautifulSoup

url = 'https://scraping-for-beginner.herokuapp.com/udemy'

respons = requests.get(url)

soup = BeautifulSoup(respons.text, 'html.parser')

n_subscriber = soup.find('p', {'class': 'subscribers'}).text
n_subscriber = int(n_subscriber.split('：')[1])

n_review = soup.find('p', {'class': 'reviews'}).text
n_review = int(n_review.split('：')[1])

print(n_subscriber, n_review)