import logging
import asyncio
from config import bot, dp, Admin
from handlers import commands, echo, fsm
from db.main_db import create_table
from handlers import commands, echo, fsm, fsm_delete

async def on_startup():
    await create_table()
    admins = Admin if isinstance(Admin, (list, tuple)) else [Admin]
    for admin_id in admins:
        await bot.send_message(chat_id=admin_id, text='Бот включен!')


dp.include_router(commands.router_commands)
dp.include_router(fsm.router_fsm)
dp.include_router(fsm_delete.router_delete)

# Эхо
dp.include_router(echo.router_echo)

dp.startup.register(on_startup)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))