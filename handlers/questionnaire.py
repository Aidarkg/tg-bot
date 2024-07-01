from aiogram import types, Dispatcher
from config import bot
from keyboards import inline_buttons


async def start_questionnaire_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="What's your favorite programming language?",
        reply_markup=await inline_buttons.start_questionnaire_keyboard()
    )


async def python_answer(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Nice choice! Why do you like Python?",
    )


async def javascript_answer(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Interesting! What projects have you worked on with JavaScript?",
    )


async def cpp_answer(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Great! How long have you been programming in C++?",
    )


def register_questionnaire_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnaire_call,
                                       lambda call: call.data == "start_questionnaire")
    dp.register_callback_query_handler(python_answer,
                                       lambda call: call.data == "python_answer")
    dp.register_callback_query_handler(javascript_answer,
                                       lambda call: call.data == "javascript_answer")
    dp.register_callback_query_handler(cpp_answer,
                                       lambda call: call.data == "cpp_answer")
