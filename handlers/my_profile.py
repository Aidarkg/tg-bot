import re
import sqlite3

from aiogram import types, Dispatcher
from config import bot
from const import PROFILE_TEXT
from database.sql_commands import Database
import random

from keyboards.inline_buttons import like_dislike_keyboard


async def show_profile_info(call: types.CallbackQuery):
    db = Database()
    user = db.sql_select_profile_user(tg_id=call.from_user.id)
    if user:
        profile_text = PROFILE_TEXT.format(
            nickname=user['nickname'],
            bio=user['biography'],
            age=user['age'],
            height=user['height'],
            weight=user['weight'],
            gender=user['gender']
        )

        photo_path = user.get('photo')
        if photo_path:
            with open(photo_path, 'rb') as photo:
                await bot.send_photo(
                    chat_id=call.message.chat.id,
                    photo=photo,
                    caption=profile_text,
                    parse_mode=types.ParseMode.MARKDOWN
                )
        else:
            await bot.send_message(
                chat_id=call.message.chat.id,
                text=profile_text,
                parse_mode=types.ParseMode.MARKDOWN
            )
    else:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Профиль не найден. Пожалуйста, пройдите регистрацию с помощью /start'
        )


async def random_profile_call(call: types.CallbackQuery):
    db = Database()
    profiles = db.sql_select_filter_profiles(
        tg_id=call.from_user.id
    )
    if profiles:
        random_profile = random.choice(profiles)
        with open(random_profile['photo'], 'rb') as photo:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=PROFILE_TEXT.format(
                    nickname=random_profile['nickname'],
                    bio=random_profile['biography'],
                    age=random_profile['age'],
                    height=random_profile['height'],
                    weight=random_profile['weight'],
                    gender=random_profile['gender']
                ),
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=await like_dislike_keyboard(owner_tg_id=random_profile['telegram_id'])
            )
    else:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='There are no more profiles'
        )


async def like_detect_call(call: types.CallbackQuery):
    db = Database()
    owner = re.sub("liker", "", call.data)
    print(call.data)
    print(owner)
    try:
        db.sql_insert_like(
            owner=owner,
            liker=call.from_user.id
        )
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f'You like user'
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='You liked this profile before'
        )
    finally:
        await random_profile_call(call=call)


async def dislike_detect_call(call: types.CallbackQuery):
    db = Database()
    owner = re.sub("disliker", "", call.data)
    print(call.data)
    print(owner)
    try:
        db.sql_insert_dislike(
            owner=owner,
            disliker=call.from_user.id
        )
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f'You dislike user'
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='You disliked this profile before'
        )
    finally:
        await random_profile_call(call=call)


def register_profile_handler(dp: Dispatcher):
    dp.register_callback_query_handler(
        show_profile_info,
        lambda call: call.data == "my_profile"
    )
    dp.register_callback_query_handler(
        random_profile_call,
        lambda call: call.data == 'random_profile'
    )
    dp.register_callback_query_handler(
        dislike_detect_call,
        lambda call: "disliker" in call.data
    )
    dp.register_callback_query_handler(
        like_detect_call,
        lambda call: "liker" in call.data
    )
