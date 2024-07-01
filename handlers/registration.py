from aiogram import types, Dispatcher
from config import bot, MEDIA
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from const import PROFILE_TEXT
from database.sql_commands import Database


class RegistrationStates(StatesGroup):
    nickname = State()
    biography = State()
    age = State()
    height = State()
    weight = State()
    gender = State()
    photo = State()


async def callback_registration_start(call: types.CallbackQuery):
    db = Database()
    user = db.sql_select_profile_user(
        tg_id=call.from_user.id
    )
    if user:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='You are already registered'
        )
    else:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Send me your Nickname, please!!!'
        )
        await RegistrationStates.nickname.set()


async def load_nickname(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text
        print(data)

    await bot.send_message(
        chat_id=message.chat.id,
        text='Tell me about yourself, please!!!'
    )
    await RegistrationStates.next()


async def load_biography(message: types.Message,
                         state: FSMContext):
    async with state.proxy() as data:
        data['biography'] = message.text
        print(data)

    await bot.send_message(
        chat_id=message.chat.id,
        text="Send me your age"
    )
    await RegistrationStates.next()


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await bot.send_message(
            chat_id=message.chat.id,
            text='Please enter your age as a number. For example: 25'
        )
        return

    async with state.proxy() as data:
        data['age'] = message.text
        print(data)

    await bot.send_message(
        chat_id=message.chat.id,
        text='Send me your height'
    )
    await RegistrationStates.next()


async def load_height(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await bot.send_message(
            chat_id=message.chat.id,
            text='Please enter your height as a number (in cm). For example: 175'
        )
        return

    async with state.proxy() as data:
        data['height'] = message.text
        print(data)

    await bot.send_message(
        chat_id=message.chat.id,
        text='Send me your weight'
    )
    await RegistrationStates.next()


async def load_weight(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await bot.send_message(
            chat_id=message.chat.id,
            text='Please enter your weight as a number (in kg). For example: 70'
        )
        return

    async with state.proxy() as data:
        data['weight'] = message.text
        print(data)

    await bot.send_message(
        chat_id=message.chat.id,
        text='Send me your gender'
    )
    await RegistrationStates.next()


async def load_gender(message: types.Message,
                      state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
        print(data)

    await bot.send_message(
        chat_id=message.chat.id,
        text='Send me your photo 😎'
    )
    await RegistrationStates.next()


async def load_photo(message: types.Message,
                     state: FSMContext):
    db = Database()
    print(message.photo)
    path = await message.photo[-1].download(
        destination_dir=MEDIA
    )
    print(path.name)
    async with state.proxy() as data:
        db.sql_insert_profile_user(
            tg_id=message.from_user.id,
            nickname=data['nickname'],
            bio=data['biography'],
            age=data['age'],
            height=data['height'],
            weight=data['weight'],
            gender=data['gender'],
            photo=path.name
        )
        with open(path.name, 'rb') as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=PROFILE_TEXT.format(
                    nickname=data['nickname'],
                    bio=data['biography'],
                    age=data['age'],
                    height=data['height'],
                    weight=data['weight'],
                    gender=data['gender']
                ),
                parse_mode=types.ParseMode.MARKDOWN
            )
        await bot.send_message(
            chat_id=message.chat.id,
            text="You have registered successfully 🙌🏻🍾🔥"
        )
        await state.finish()


def register_registration_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        callback_registration_start,
        lambda call: call.data == "registration"
    )
    dp.register_message_handler(
        load_nickname,
        state=RegistrationStates.nickname,
        content_types=['text']
    )
    dp.register_message_handler(
        load_biography,
        state=RegistrationStates.biography,
        content_types=['text']
    )
    dp.register_message_handler(
        load_age,
        state=RegistrationStates.age,
        content_types=['text']
    )
    dp.register_message_handler(
        load_height,
        state=RegistrationStates.height,
        content_types=['text']
    )
    dp.register_message_handler(
        load_weight,
        state=RegistrationStates.weight,
        content_types=['text']
    )
    dp.register_message_handler(
        load_gender,
        state=RegistrationStates.gender,
        content_types=['text']
    )
    dp.register_message_handler(
        load_photo,
        state=RegistrationStates.photo,
        content_types=types.ContentTypes.PHOTO
    )
