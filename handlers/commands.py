from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from config import bot
from handlers.buttons import main_buttons, main_builder, menu_inline

router_commands = Router()

@router_commands.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Привет. Напиши своё имя', reply_markup=menu_inline)
    await message.answer(f'Привет. Твой ID — {message.from_user.id}')


@router_commands.message(Command('help'))
async def help_command(message: Message):
    await message.answer('/start - старт бота \n/help - помощник ')


@router_commands.message(F.text == 'привет')
async def hello_command(message: Message):
    await message.answer('Hello')


@router_commands.message(Command('mem'))
async def mem_command(message: Message):
    photo = FSInputFile('media/mem.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@router_commands.callback_query(F.data == 'mem')
async def mem_command(call: CallbackQuery):
    photo = FSInputFile('media/mem.png')
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo)
    await call.answer()
