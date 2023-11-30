from bs4 import BeautifulSoup
import requests

web_data = requests.get(
    "https://www.freecodecamp.org/news/python-requirementstxt-explained/",
    timeout=100
)
soup = BeautifulSoup(web_data.content, features="html.parser")
news_info = soup.findAll("p")
for news in news_info:
    print(news.text)
