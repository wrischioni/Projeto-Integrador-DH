# tool kit
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
from time import sleep
from datetime import datetime as dt


class INVESTING:

    def __init__(self, n_last_page):
        # ~ attributes for Investing web page scraping application
        self.url_home = 'https://br.investing.com'  # main web page url
        self.url_news = 'https://br.investing.com/news/economy-news'  # news url
        self.url_gov_news = 'https://br.investing.com/news/politics-news'    # news url (politics)
        self.url_page = '/'  # url page number complement
        self.n_last_page = n_last_page  # last news page
        self.session = HTMLSession()

    def get_html_content(self, news_type='economy', page_n=None, first=True):
        if news_type == 'economy':
            if first is True:
                html_raw = self.session.get(self.url_news)
            else:
                html_raw = self.session.get(f'{self.url_news}{self.url_page}{page_n}')
        else:
            if first is True:
                html_raw = self.session.get(self.url_gov_news)
            else:
                html_raw = self.session.get(f'{self.url_gov_news}{self.url_page}{page_n}')
        html_preprocessed = BeautifulSoup(html_raw.html.html, 'html.parser')
        return html_preprocessed

    @staticmethod
    def get_news_url(html):
        news = html.find_all('div', {'class': 'largeTitle'})
        links = [a['href'] for a in news[0].find_all('a', {'class': 'title'}, href=True)]   # news links
        return links

    def get_news_info(self, link):
        html_page_raw = self.session.get(self.url_home + link)
        html_news = BeautifulSoup(html_page_raw.html.html, 'html.parser')
        title_content = html_news.find_all('section', {'id': 'leftColumn'})[0]
        title = title_content.find_all('h1', {'class': 'articleHeader'})[0].text
        header_content = html_news.find_all('div', {'class': 'contentSectionDetails'})[0]
        news_type = header_content.find_all('a')[0].text
        date_time = header_content.find_all('span')[0].text
        body_content = html_news.find_all('div', {'class': 'WYSIWYG articlePage'})[0]
        image_content = body_content.find_all('div', {'id', 'imgCarousel'})[0]
        image_title = image_content.find_all('span', {'class', 'text'})[0].text
        content = [p.text for p in body_content.find_all('p')]
        return {'date_time': date_time,
                'type': news_type,
                'image_title': image_title,
                'title': title,
                'content': content
                }

    def full_extraction(self, news_tag):
        print(f'process start at: {dt.now()}')
        print('------------------')
        all_news = []
        for i in range(1, (self.n_last_page + 1)):
            if i == 1:
                page_html = self.get_html_content()
            else:
                page_html = self.get_html_content(news_type=news_tag, page_n=i, first=False)
            link_list = self.get_news_url(html=page_html)
            print(f'{i}th-iteration: ', end='')
            print(f'get-links completed at: {dt.now().hour:2>}:{dt.now().minute:2>} / loading content: ', end='')
            for link_ref in link_list:
                try:
                    news_info = self.get_news_info(link_ref)
                except:
                    continue
                all_news.append(news_info.copy())
                print('|', end='')
                sleep(random.uniform(0.0, 0.8))
            print(f' / get-news completed at: {dt.now().hour:2>}:{dt.now().minute:2>}')
        print('------------------')
        print(f'full-job at: {dt.now()}')
        return all_news
