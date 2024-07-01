from aiogram import executor
from config import dp
from handlers import (
    start,
    questionnaire,
    chat_actions,
    ban_users,
    registration,
    my_profile,
    reference,
    scraper,
    youtube_download
)
from database import sql_commands


async def on_startup(_):
    db = sql_commands.Database()
    db.sql_create_tables()


start.register_start_handlers(dp=dp)
questionnaire.register_questionnaire_handlers(dp=dp)
ban_users.register_ban_users_handlers(dp=dp)
my_profile.register_profile_handler(dp=dp)
registration.register_registration_handlers(dp=dp)
reference.register_reference_users(dp=dp)
scraper.register_scraper_handler(dp=dp)
youtube_download.register_audio_handler(dp=dp)
chat_actions.register_chat_actions_handlers(dp=dp)

if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )
