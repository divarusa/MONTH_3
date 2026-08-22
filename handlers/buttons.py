from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/start'), KeyboardButton(text='/help'), 
         KeyboardButton(text='/mem'), KeyboardButton(text='Ничего')],
    ],
    resize_keyboard=True
)


main_buttons_builder = ReplyKeyboardBuilder()
main_buttons_builder.button(text='/start')
main_buttons_builder.button(text='/help')
main_buttons_builder.adjust(2)

main_builder = main_buttons_builder.as_markup(resize_keyboard=True)



menu_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Мем', callback_data='mem')],
        [InlineKeyboardButton(text='Помощь', callback_data='help')]
    ]
)

confirm_delete = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да, удалить', callback_data='confirm_delete'),
         InlineKeyboardButton(text='Отмена', callback_data='cancel_delete')]
    ]
)

def user_actions(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Удалить', callback_data=f'delete:{user_id}')]
        ]
    )