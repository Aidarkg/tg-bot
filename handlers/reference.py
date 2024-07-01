from aiogram import types, Dispatcher
from config import bot
from keyboards.inline_buttons import referral_program_keyboard
from database.sql_commands import Database
import os
import binascii
from aiogram.utils.deep_linking import _create_link


async def callback_referral_program(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Welcome to the Referral Program! Choose an option below:',
        reply_markup=await referral_program_keyboard()
    )


async def callback_referral_link(call: types.CallbackQuery):
    db = Database()
    user = db.sql_select_user(
        tg_id=call.from_user.id
    )
    print(user)

    if not user['link']:
        token = binascii.hexlify(os.urandom(8)).decode()
        link = await _create_link(link_type="start", payload=token)
        db.sql_update_user_link(
            link=link,
            tg_id=call.from_user.id,
        )
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f"Your referral link: {link}"
        )
    else:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f"Your referral link: {user['link']}"
        )


async def callback_referral_list(call: types.CallbackQuery):
    db = Database()
    referral_list = db.get_referral_list(
        user_id=call.from_user.id
    )
    if referral_list:
        message = "Your referral list:\n"
        for user in referral_list:
            message += f"- {user[1]} ({user[0]})\n"
    else:
        message = "You don't have any referrals yet."

    await bot.send_message(
        chat_id=call.message.chat.id,
        text=message
    )


def register_reference_users(dp: Dispatcher):

    dp.register_callback_query_handler(
        callback_referral_program,
        lambda call: call.data == "referral_program"
    )

    dp.register_callback_query_handler(
        callback_referral_link,
        lambda call: call.data == "referral_link"
    )

    dp.register_callback_query_handler(
        callback_referral_list,
        lambda call: call.data == "referral_list"
    )
