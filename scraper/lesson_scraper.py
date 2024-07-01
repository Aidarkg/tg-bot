import asyncio
from parsel import Selector
import httpx
from pprint import pprint


class NewsScraper:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    URL = 'https://animespirit.tv/'
    LINK_XPATH = '//div[@class="custom-poster"]/div/a/@href'

    def __init__(self):
        self.links = []

    async def get_html(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            result = self.parse_news(response.text)
            self.links.extend(result)

    def parse_news(self, response):
        selector = Selector(text=response)
        all_links = selector.xpath(self.LINK_XPATH).getall()

        return all_links


async def main():
    scraper = NewsScraper()
    pages = []
    for i in range(1, 25):
        url = f"https://animespirit.tv/page/{i}/"
        task = asyncio.create_task(scraper.get_html(url))
        pages.append(task)

    await asyncio.gather(*pages)

    pprint(scraper.links[:5])


if __name__ == '__main__':
    asyncio.run(main())