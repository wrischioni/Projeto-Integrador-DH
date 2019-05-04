# tool kit
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep as s
from datetime import datetime as dt

gecko_path = r'./geckodriver'


class VALOR:

    def __init__(self, ff_driver=str()):
        self.url_home = 'https://www.valor.com.br'
        self.url_news = 'https://www.valor.com.br/brasil/macroeconomia'
        self.url_page = '?page='
        self.n_last_page = 2480
        self.ff_driver = ff_driver
        self.driver = wd.Firefox(executable_path=self.ff_driver)

    def navigate(self, page=None, first=True):
        if first is True:
            self.driver.get(self.url_news)
        else:
            self.driver.get(self.url_news + self.url_page + page)

    def get_news_url(self):
        html_raw = self.driver.page_source
        html = bs(html_raw, 'html.parser')
        news = html.find_all('div', {'class': 'mdl manchete'})
        links = [a['href'] for a in news[0].find_all('a', href=True) if a['href'][-8:] != 'comments']
        return links

    def get_news_info(self, link):
        self.driver.get(self.url_home + link)
        html_page_raw = self.driver.page_source
        html_news = bs(html_page_raw, 'html.parser')
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

    def full_crawler(self):
        print(f'process start at: {dt.now()}')
        print('------------------')
        all_news = []
        for i in range(0, (self.n_last_page + 1)):
            if i == 0:
                self.navigate()
            else:
                i_char = str(i)
                self.navigate(page=i_char, first=False)
            link_list = self.get_news_url()
            print(f'{i}th-iteration: ', end='')
            print(f'get-links completed at: {dt.now().hour:2>}:{dt.now().minute:2>} / loading content: ', end='')
            for link_ref in link_list:
                news_info = self.get_news_info(link_ref)
                all_news.append(news_info.copy())
                print('|', end='')
            print(f' / get-news completed at: {dt.now().hour:2>}:{dt.now().minute:2>}')
            if i == 1:
                break
        print('------------------')
        print(f'full-job at: {dt.now()}')
        return all_news

    def to_pandas(self, news_dataset, export=False):
        df = pd.DataFrame(news_dataset)
        if export is True:
            tf = dt.now().time()
            df.to_csv(f'./valor_economico_news_{tf}.csv')


# exempplo
ex = VALOR(gecko_path)
test = ex.full_crawler()
for n in test:
    print(n)
df = pd.DataFrame(test)
print(df)
