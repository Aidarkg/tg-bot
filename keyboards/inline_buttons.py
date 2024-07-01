from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_menu_keyboard():
    markup = InlineKeyboardMarkup()
    questionnaire_button = InlineKeyboardButton(
        "Start Questionnaire 🔥",
        callback_data="start_questionnaire"
    )
    ban_button = InlineKeyboardButton(
        "Ban Users 🚫",
        callback_data="ban_users"
    )
    registration_button = InlineKeyboardButton(
        "Registration 🐉",
        callback_data="registration"
    )
    my_profile_button = InlineKeyboardButton(
        "My profile 😎",
        callback_data="my_profile"
    )
    view_profile_button = InlineKeyboardButton(
        "View Profiles 👍🏻👎🏻",
        callback_data="random_profile"
    )
    referral_program_button = InlineKeyboardButton(
        "Referral Program 🔄",
        callback_data="referral_program"
    )
    scraper_button = InlineKeyboardButton(
        "Anime Link ☯☯",
        callback_data="scraper_button"
    )
    download_audio = InlineKeyboardButton(
        "Youtube MP3 🎧",
        callback_data="audio_download_button"
    )
    markup.add(ban_button)
    markup.add(questionnaire_button)
    markup.add(registration_button)
    markup.add(my_profile_button)
    markup.add(view_profile_button)
    markup.add(referral_program_button)
    markup.add(scraper_button)
    markup.add(download_audio)
    return markup


async def start_questionnaire_keyboard():
    markup = InlineKeyboardMarkup()
    python_button = InlineKeyboardButton(
        "Python 🐍",
        callback_data="python_answer"
    )
    javascript_button = InlineKeyboardButton(
        "JavaScript 💻",
        callback_data="javascript_answer"
    )
    cpp_button = InlineKeyboardButton(
        "C++ 💡",
        callback_data="cpp_answer"
    )
    markup.add(python_button)
    markup.add(javascript_button)
    markup.add(cpp_button)
    return markup


async def like_dislike_keyboard(owner_tg_id):
    markup = InlineKeyboardMarkup()
    like_button = InlineKeyboardButton(
        "LIKE 👍🏻",
        callback_data=f"liker{owner_tg_id}"
    )
    dislike_button = InlineKeyboardButton(
        "DISLIKE 👎🏻",
        callback_data=f"disliker{owner_tg_id}"
    )
    markup.add(like_button)
    markup.add(dislike_button)
    return markup


async def referral_program_keyboard():
    markup = InlineKeyboardMarkup()
    referral_link_button = InlineKeyboardButton(
        "Referral Link 🔗",
        callback_data="referral_link"
    )
    referral_list_button = InlineKeyboardButton(
        "Referral List 📋",
        callback_data="referral_list"
    )
    markup.add(referral_link_button)
    markup.add(referral_list_button)
    return markup