import re
from bs4 import BeautifulSoup

import urllib.parse


class HtmlParser(object):

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    @staticmethod
    def _get_new_urls(page_url, soup):  # 获取页面中其他词条的URL列表
        new_urls = set()

        links = soup.find_all('a', href=re.compile(r"/item/(.*)"))  # 搜集所有符合格式的URL
        print('links len is:', len(links))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)  # 拼接URL
            new_urls.add(new_full_url)
        return new_urls

    @staticmethod
    def _get_new_data(page_url, soup):

        res_data = {'url': page_url}

        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        res_data['title'] = title_node.get_text()

        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()

        return res_data
