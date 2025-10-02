import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class BookScraper:
    def __init__(self):
        self.base_url = 'https://books.toscrape.com/catalogue/page-{}.html'
        self.books = []

    def scrape_page(self, page_num):
        ''' Scrape a single page'''
        url = self.base_url.format(page_num)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article', class_='product_pod')

            for article in articles:
                book = {
                    'title': article.h3.a['title'],
                    'price': article.find('p', class_='price_color').text,
                    'rating': article.p['class'][1],
                    'availability': article.find('p', class_='instock availability').text.strip(),
                }
                self.books.append(book)
                print(f"Scraped page {page_num}")

        else:
            print(f"Failed to scrape page {page_num}")

    def scrape_all_pages(self, num_page=50):
        '''Scrape multiple pages'''
        for page in range(1, num_page+1):
            self.scrape_page(page)
            time.sleep(0.5)

    def save_to_csv(self, filename='books.csv'):
        '''Save the scraped data to a csv file'''
        df = pd.DataFrame(self.books)
        df.to_csv(filename, index=False)
        print(f'Saved {len(self.books)} books to {filename}')

if __name__ == '__main__':
    scraper = BookScraper()
    scraper.scrape_all_pages(5)
    scraper.save_to_csv()