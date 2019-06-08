# tool kit
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import numpy as np
import random
from time import sleep
from datetime import datetime as dt


class G1:

    def __init__(self, n_last_page):
        self.url_page = f'https://g1.globo.com/economia/index/feed/pagina-'
        self.url_complement = '.ghtml'
        self.log = []
        self.last_page = n_last_page
        self.session = HTMLSession()

    def get_html_content(self, n_page):
        html_raw = self.session.get(f'{self.url_page}{n_page}{self.url_complement}')
        html_preprocessed = BeautifulSoup(html_raw.html.html, 'html.parser')
        return html_preprocessed

    @staticmethod
    def get_news_url(html_txt):
        news_list = html_txt.findAll('a', {'class': 'feed-post-link gui-color-primary gui-color-hover'})
        href_list = [link['href'] for link in news_list]
        return href_list

    def get_news_info(self, link):
        html_page_raw = self.session.get(link)
        html_news = BeautifulSoup(html_page_raw.html.html, 'html.parser')
        try:
            title = html_news.find_all('h1', {'class': 'content-head__title'})[0].text
        except Exception as e:
            title = np.nan
            # self.log.append({'link': link, 'variable': 'title', 'error': e})
        try:
            subtitle = html_news.find_all('h2', {'class': 'content-head__subtitle'})[0].text
        except Exception as e:
            subtitle = np.nan
            # self.log.append({'link': link, 'variable': 'subtitle', 'error': e})
        try:
            author = html_news.find_all('p', {'class': 'content-publication-data__from'})[0].text
        except Exception as e:
            author = np.nan
            # self.log.append({'link': link, 'variable': 'author', 'error': e})
        try:
            date_time = html_news.find_all('p', {'class': 'content-publication-data__updated'})[0].text
        except Exception as e:
            date_time = np.nan
            # self.log.append({'link': link, 'variable': 'date_time', 'error': e})
        try:
            content = html_news.find_all\
            ('p', {'class': 'content-text__container theme-color-primary-first-letter'})[0].text
        except Exception as e:
            content = np.nan
            # self.log.append({'link': link, 'variable': 'content', 'error': e})
        news_content = html_news.find_all('p')
        full_content = [content_box.text for content_box in news_content]
        return {'date_time': date_time,
                'title': title,
                'subtitle': subtitle,
                'author': author,
                'content': content,
                'full_content': full_content}

    def full_extraction(self):

        print(f'process start at: {dt.now()}')  # process control*
        print('------------------')
        # ~ combine all functions to extract all news from all pages
        all_news = []   # news data set
        # going from 1th page till last_page attribute
        for i in range(1, (self.last_page + 1)):
            try:
                page_html = self.get_html_content(n_page=i)
                urls = self.get_news_url(html_txt=page_html)

                print(f'{i}th-iteration: ', end='')      # process control*
                print(f'get-links completed at: {dt.now().hour:2>}:{dt.now().minute:2>} / loading content: ', end='')
                # get news attributes and stores into all_news list
                for url in urls:
                    news_content = self.get_news_info(url)
                    all_news.append(news_content.copy())
                    print('|', end='')   # process control*
                    sleep(random.uniform(0.0, 0.8))
            except:
                continue
            print(f' / get-news completed at: {dt.now().hour:2>}:{dt.now().minute:2>}')     # process control*
        print('------------------')     # process control*
        print(f'full-job at: {dt.now()}')
        # return final data set with all news dicts included
        return all_news
