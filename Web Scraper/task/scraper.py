import requests
import os
from bs4 import BeautifulSoup

number_of_pages = int(input("Enter the number of pages you want to scrape: "))
type_of_article = str(input("Enter the type of article you want to scrape: "))

base_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"


def scrape_page(number_of_pages, type_of_article):
    for i in range(1, number_of_pages + 1):
        response = requests.get(base_url + f"&page={i}")
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        for article in soup.find_all('article'):
            folder = "Page_" + str(i)
            os.makedirs(folder, exist_ok=True)
            typ_e = article.find('span', class_='c-meta__type').text
            if typ_e == type_of_article:
                link = article.find('a').get('href')
                get_article = requests.get("https://www.nature.com/nature" + link)
                soup = BeautifulSoup(get_article.content, 'html.parser')
                heading = soup.find('meta', property="og:title").get('content')
                filename = heading.replace(' ', '_') + '.txt'
                file_path = os.path.join(folder, filename)
                text = soup.find('p', class_="article__teaser").text
                file = open(file_path, "wb")
                file.write(text.encode())
                file.close()

scrape_page(number_of_pages, type_of_article)




