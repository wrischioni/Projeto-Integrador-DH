# tool kit
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
from time import sleep
from datetime import datetime as dt


class VALOR:

    def __init__(self, n_last_page):
        # ~ attributes for Valor Economico web page scraping application
        self.url_home = 'https://www.valor.com.br'     # main web page
        self.url_news = 'https://www.valor.com.br/brasil/macroeconomia'     # url news type complement
        self.url_page = '?page='    # url page number complement
        self.n_last_page = n_last_page     # last news page
        self.session = HTMLSession()

    def get_html_content(self, page_n=None, first=True):
        if first is True:
            html_raw = self.session.get(self.url_news)
        else:
            html_raw = self.session.get(f'{self.url_news}{self.url_page}{page_n}')
        html_preprocessed = BeautifulSoup(html_raw.html.html, 'html.parser')
        return html_preprocessed

    @staticmethod
    def get_news_url(html):
        news = html.find_all('div', {'class': 'mdl manchete'})
        links = [a['href'] for a in news[0].find_all('a', href=True) if a['href'][-8:] != 'comments']
        return links

    def get_news_info(self, link):
        html_page_raw = self.session.get(self.url_home + link)
        html_news = BeautifulSoup(html_page_raw.html.html, 'html.parser')
        body_content = html_news.find_all('div', {'class': 'node-inner'})[0]
        header_content = body_content.find_all('div', {'class': 'n-header'})[0]
        date_time = header_content.find_all('span')[0].text
        title = header_content.find_all('h1')[0].text
        author_site = body_content.find_all('div', {'class': 'node-author-inner'})[0].text
        content = body_content.find_all('div', {'id': 'node-body'})[0].text
        return {'date_time': date_time,
                'title': title,
                'author_site': author_site,
                'content': content}

    def full_extraction(self):

        print(f'process start at: {dt.now()}')
        print('------------------')
        all_news = []
        for i in range(0, (self.n_last_page)):
            if i == 0:
                page_html = self.get_html_content()
            else:
                page_html = self.get_html_content(page_n=i, first=False)

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
