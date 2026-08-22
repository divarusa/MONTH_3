from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from config import bot
from handlers.buttons import menu_inline
from db import main_db
from handlers import buttons

router_commands = Router()


@router_commands.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Привет. Напиши своё имя', reply_markup=menu_inline)
    await message.answer(f'Привет. Твой ID - {message.from_user.id}')


@router_commands.message(Command('help'))
async def help_command(message: Message):
    await message.answer('/start - старт бота \n/help - помощник \n/form - заполнить анкету \n/users - список записей')


@router_commands.message(F.text == 'привет')
async def hello_command(message: Message):
    await message.answer('Hello')


@router_commands.message(Command('mem'))
async def mem_command(message: Message):
    photo = FSInputFile('media/mem.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@router_commands.message(Command('users'))
async def show_users_command(message: Message):
    users = await main_db.get_all_users_with_info()
    if not users:
        await message.answer("База данных пока пуста.")
        return

    for user in users:
        caption = (
            f"ID: {user['id']}\n"
            f"Имя: {user['name']}\n"
            f"Возраст: {user['age']}\n"
            f"Телефон: {user['phone']}\n"
            f"Город: {user['city']}"
        )
        if user['photo_id']:
            await message.answer_photo(
                photo=user['photo_id'], 
                caption=caption,
                reply_markup=buttons.user_actions(user['id'])
            )
        else:
            await message.answer(caption)