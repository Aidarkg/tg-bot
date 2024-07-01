import pytube.exceptions
from aiogram import types
from aiogram.dispatcher import Dispatcher
from pytube import YouTube
from config import bot, ADMIN_ID
from pytube.exceptions import AgeRestrictedError
from database.sql_commands import Database
from datetime import timedelta, datetime
from profanity_check import predict_prob
import requests
from io import BytesIO



async def process_audio(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Пожалуйста, отправьте мне ссылку на видео с YouTube.")


async def download_yt_audio(message: types.Message):
    db = Database()
    user_id = message.from_user.id

    try:
        yt = YouTube(message.text)
        audio_buffer = BytesIO()

        sent_message = await bot.send_message(
            chat_id=message.chat.id,
            text="Загрузка началась. Пожалуйста, подождите..."
        )

        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.stream_to_buffer(buffer=audio_buffer)
        audio_buffer.seek(0)

        # Загрузка изображения как обложки аудио
        thumb_buffer = BytesIO(requests.get(yt.thumbnail_url).content) if yt.thumbnail_url else None

        db.insert_table_music(
            music_name=yt.title,
            user_name=message.chat.first_name,
            tg_id=user_id
        )

        await bot.send_audio(
            chat_id=message.chat.id,
            audio=types.InputFile(audio_buffer, filename=yt.title),
            thumb=types.InputFile(thumb_buffer, filename=yt.title) if thumb_buffer else None,
            parse_mode=types.ParseMode.MARKDOWN
        )

        await bot.delete_message(
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id
        )
        audio_buffer.close()
        thumb_buffer.close()

    except AgeRestrictedError:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Видео ограничено по возрасту и не может быть загружено без аутентификации. Пожалуйста, предоставьте мне другую ссылку."
        )
    except pytube.exceptions.RegexMatchError:
        await chat_messages(message)
    except pytube.exceptions.VideoUnavailable:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Видео недоступно. Пожалуйста, предоставьте мне другую ссылку."
        )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Произошла ошибка: {e}. Пожалуйста, предоставьте мне другую ссылку."
        )


async def chat_messages(message: types.Message):
    db = Database()
    if message.chat.id == int(message.chat.id):
        ban_word_predict_prob = predict_prob([message.text])
        print(ban_word_predict_prob)
        if ban_word_predict_prob[0] > 0.5:
            user = db.sql_select_ban_user(
                tg_id=message.from_user.id
            )
            print(user)
            if not user:
                db.sql_insert_ban_user(
                    tg_id=message.from_user.id
                )
            elif int(user['count']) >= 3:
                if user['telegram_id'] == int(ADMIN_ID):
                    pass
                else:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="You r banned"
                    )
                    await bot.ban_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        until_date=datetime.now() + timedelta(seconds=100)
                    )
                    db.sql_delete_user(
                        tg_id=message.from_user.id
                    )
            else:
                db.sql_update_ban_user_count(
                    tg_id=message.from_user.id
                )

            await message.delete()
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"You have cursed this is not allowed in this group!\n"
                     f"User: {message.from_user.first_name}\n"
                     f"In third you will be banned"
            )


def register_audio_handler(dp: Dispatcher):
    dp.register_callback_query_handler(
        process_audio,
        lambda call: call.data == "audio_download_button")
    dp.register_message_handler(
        download_yt_audio, content_types=types.ContentTypes.TEXT)
