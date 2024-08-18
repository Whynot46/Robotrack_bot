from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Main_keyboard')]],
    resize_keyboard=True)


download_keyboard = track_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="download_keyboard", callback_data=f"was_download")]
    ])