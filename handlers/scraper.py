from parsel import Selector
from aiogram import types, Dispatcher
from config import bot
import requests


async def parse_date(call: types.CallbackQuery):
    URL = 'https://animespirit.tv/'
    LINK_XPATH = '//div[@class="custom-poster"]/a/@href'
    TEXT_XPATH = '//h1/text()'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    html = requests.get(url=URL, headers=headers).text
    tree = Selector(text=html)
    links = tree.xpath(LINK_XPATH).getall()
    for link in links[:5]:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=link
        )


def register_scraper_handler(dp: Dispatcher):
    dp.register_callback_query_handler(
        parse_date,
        lambda call: call.data == "scraper_button"
    )
