import logging
from config import bot, dp, Admin
import asyncio
from handlers import commands, echo, fsm

async def on_startup():
    for admin_id in Admin:
        await bot.send_message(chat_id=admin_id, text='Бот включен!')

dp.include_router(commands.router_commands)
dp.include_router(fsm.router_fsm)

# Эхо 
dp.include_router(echo.router_echo)

dp.startup.register(on_startup)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))