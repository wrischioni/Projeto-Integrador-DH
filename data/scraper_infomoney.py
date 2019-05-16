# tool kit
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
from time import sleep
from datetime import datetime as dt


class INFOM:

    def __init__(self, n_last_page):
        # ~ attributes for Infomoney web page scraping application
        self.url_home = 'https://www.infomoney.com.br'  # main web page
        self.company_list = ['santanderbr', 'itauunibanco', 'bradesco']     # url company complement
        self.last_page = n_last_page     # last news webpage for selected company
        self.session = HTMLSession()    # request session

    def get_html_content(self, company, page_n):
        # ~ get html content from a single news web page (composed of 7 news in average )
        # get the html from request session
        html_raw = self.session.get(f'{self.url_home}/{company}/noticias/{page_n}#noticias')
        # parsing html with b.soup (bs)
        html_preprocessed = BeautifulSoup(html_raw.html.html, 'html.parser')
        # returning news page html
        return html_preprocessed

    @staticmethod
    def get_news_url(html_txt):
        # ~ get html with all news links from that page
        news_list = html_txt.findAll('div', {'id': 'StockNews'})[0]
        # extract 'a' tags with news url (href)
        news_links = news_list.findAll('a', {'id': 'hlkTempC'})
        # made a list of all news urls
        href_list = [link['href'] for link in news_links]
        return href_list

    def get_news_info(self, url):
        # ~ get html content by session request, using main web page url and news url combined
        html_news_raw = self.session.get(f'{self.url_home}{url}')
        html_news = BeautifulSoup(html_news_raw.html.html, 'html.parser')
        # ~ get news header html, use it to extract news attributes as:
        html_header = html_news.find_all('div', {'class': 'column large-12'})[0]
        news_author = html_header.find_all('span', {'class': 'article__author'})[0].text    # news author name;
        html_tags = html_header.find_all('span', {'class': 'article__breadcrumbs'})[0]
        news_tags = [tag.text for tag in html_tags.find_all('a')]   # list of tags (segment of news);
        news_date_time = html_header.find_all('span', {'id': 'article-date'})[0].text   # news date and time submission;
        news_title = html_header.find_all('h1')[0].text     # news title;
        news_subtitle = html_header.find_all('p')[0].text   # and news subtitle
        # ~ get news header html, use it to extract news body text content:
        html_body = html_news.find_all('div', {'class': 'article__content'})[0]
        # removing all java script code from body text
        for java_script in html_body(["script", "style"]):
            java_script.decompose()
        news_body = html_body.text      # news body text
        # returning a dict with all news attributes mentioned
        return {'author': news_author,
                'tags': news_tags,
                'date_time': news_date_time,
                'title': news_title,
                'subtitle': news_subtitle,
                'body': news_body
                }

    def full_extraction(self, company_name):

        print(f'process start at: {dt.now()}')  # process control*
        print('------------------')
        # ~ combine all functions to extract all news from all pages
        all_news = []   # news data set
        # going from 1th page till last_page attribute
        for i in range(1, (self.last_page + 1)):
            page_html = self.get_html_content(company=company_name, page_n=i)
            urls = self.get_news_url(html_txt=page_html)

            print(f'{i}th-iteration: ', end='')      # process control*
            print(f'get-links completed at: {dt.now().hour:2>}:{dt.now().minute:2>} / loading content: ', end='')
            # get news attributes and stores into all_news list
            for url in urls:
                news_content = self.get_news_info(url)
                all_news.append(news_content.copy())
                print('|', end='')   # process control*
                sleep(random.uniform(0.0, 0.8))

            print(f' / get-news completed at: {dt.now().hour:2>}:{dt.now().minute:2>}')     # process control*
        print('------------------')     # process control*
        print(f'full-job at: {dt.now()}')
        # return final data set with all news dicts included
        return all_news
