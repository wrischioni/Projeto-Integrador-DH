# tool kit
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
from time import sleep
from datetime import datetime as dt


class ADVFN:

    def __init__(self, first_page, last_page):
        # ~ attributes for ADVFN web page scraping application
        # 1th url news web page
        self.first_page = first_page
        self.last_page = last_page
        self.url_1th_page = \
        'http://br.advfn.com/jornal/economia-e-politica/brasil?xref=economia-e-politica-landing-page'
        self.url_page = '&paged='     # 2th+ url news web page
        self.session = HTMLSession()

    def get_html_content(self, page_n=None):
        html_raw = self.session.get(f'{self.url_1th_page}{self.url_page}{page_n}')
        html_preprocessed = BeautifulSoup(html_raw.html.html, 'html.parser')
        return html_preprocessed

    @staticmethod
    def get_news_url(html):
        news = html.find_all('div', {'class': 'posts-list listing-alt'})
        links = [a['href'] for a in news[0].find_all('a', {'class': 'post-title'}, href=True)]
        return links

    def get_news_info(self, link):
        html_page_raw = self.session.get(link)
        html_news = BeautifulSoup(html_page_raw.html.html, 'html.parser')
        body_news = html_news.find_all('div', {'class': 'col-8 main-content'})[0]
        segment = body_news.find_all('span', {'class': 'cat-title'})[0].text
        date_time = body_news.find_all('time', {'class': 'post-date'})[0].text
        comments = body_news.find_all('a', {'class': 'comments'})[0].text
        title = body_news.find_all('h1', {'class': 'post-title'})[0].text
        author = body_news.find_all('span', {'class': 'posted-by'})[0].text
        body_content = body_news.find_all('div', {'class': 'post-content post-dymamic'})[0]
        content = [p.text for p in body_content.find_all('p')]
        return {'type': segment,
                'date_time': date_time,
                'title': title,
                'author_site': author,
                'content': content,
                'n_coments': comments}

    def full_extraction(self):
        print(f'process start at: {dt.now()}')
        print('------------------')
        all_news = []
        for i in range(self.first_page, (self.last_page + 1)):
            page_html = self.get_html_content(page_n=i)
            link_list = self.get_news_url(html=page_html)
            print(f'{i}th-iteration: ', end='')
            print(f'get-links completed at: {dt.now().hour:2>}:{dt.now().minute:2>} / loading content: ', end='')
            for link_ref in link_list:
                news_info = self.get_news_info(link_ref)
                all_news.append(news_info.copy())
                print('|', end='')
                sleep(random.uniform(0.0, 0.8))
            print(f' / get-news completed at: {dt.now().hour:2>}:{dt.now().minute:2>}')
        print('------------------')
        print(f'full-job at: {dt.now()}')
        return all_news
