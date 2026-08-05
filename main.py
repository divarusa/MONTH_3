import random
from datetime import datetime

from decouple import config

from aiogram import Bot, Dispatcher, Router, F
import asyncio
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import logging

token = config('BOT_TOKEN')

router = Router()


@router.message(Command('start'))
async def start_command(message: Message, bot: Bot):
    await message.answer('Привет. Напиши своё имя ')
    await bot.send_message(chat_id=message.chat.id, text='Приветствую!')


@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer(
        "/start — Старт бота\n"
        "/time — Текущее время\n"
        "/random — Случайное число\n"
        "/joke — Смешной мем\n"
        "/mem — Картинка с мемом\n"
        "/help — Помощник"
    )
@router.message(F.text == 'привет')
async def hello_command(message: Message):
    await message.answer('Hello')


@router.message(Command('mem'))
async def mem_command(message: Message, bot: Bot):
    photo = FSInputFile('media/mem.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@router.message(Command('time'))
async def time_command(message: Message):
    now = datetime.now().strftime('%d.%m.%y %H:%M')
    await message.answer(f'Сейчас: {now}')

@router.message(Command('random'))
async def random_command(message: Message):
    number = random.randint(1, 100)
    await message.answer(f'Твое случайное число: {number}')

@router.message(Command('joke'))
async def joke_command(message: Message):
    jokes = [
        'Колобок повесился.',
        'Русалка села на шпагат.',
        'Буратино утонул.'
        'Заходит улитка в бар... а та бармен.',
        'Купил мужик шляпу, а она ему как раз.'
    ]
    await message.answer(random.choice(jokes))






@router.message(F.text)
async def echo(message: Message):
    await message.answer(f'Такой команды нет - {message.text}')


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

