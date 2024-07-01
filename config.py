from aiogram import Dispatcher, Bot
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# PROXY_URL = 'http://proxy.server:3128'
storage = MemoryStorage()
TOKEN = config("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
GROUP_ID = config("GROUP_ID")
GROUP_ID2 = config("GROUP_ID2")
ADMIN_ID = config("ADMIN_ID")
MEDIA = config("MEDIA")
AUDIO = config("AUDIO")
