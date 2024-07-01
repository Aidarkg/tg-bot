from parsel import Selector
import requests


class NewScraper:
    URL = 'https://animespirit.tv/'
    LINK_XPATH = '//div[@class="custom-poster"]/a/@href'
    TEXT_XPATH = '//h1/text()'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    def parse_date(self):
        html = requests.get(url=self.URL, headers=self.headers).text
        tree = Selector(text=html)
        links = tree.xpath(self.LINK_XPATH).getall()
        for link in links[:5]:
            return link


if __name__ == '__main__':
    scraper = NewScraper()
    scraper.parse_date()
