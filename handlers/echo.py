from aiogram import Router, types
from aiogram.fsm.context import FSMContext

router_echo = Router()

@router_echo.message(lambda message: message.text and message.text.startswith('/'))
async def echo_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        return

    known = {'/start', '/help', '/mem', '/users', '/form', '/cancel'}
    cmd = message.text.split()[0].lower()
    if cmd in known:
        return

    await message.answer(f"Такой команды нет - {message.text}")