from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db import main_db
from handlers import buttons

router_delete = Router()


class DeleteUser(StatesGroup):
    confirm = State()


@router_delete.callback_query(F.data.startswith('delete:'))
async def delete_start(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(':')[1]

    await state.update_data(user_id=user_id)
    await call.message.answer('Точно удалить эту запись?', reply_markup=buttons.confirm_delete)
    await call.answer()
    await state.set_state(DeleteUser.confirm)


@router_delete.callback_query(DeleteUser.confirm, F.data == 'confirm_delete')
async def delete_confirm(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']

    await main_db.delete_user_db(user_id)

    await call.message.answer('Запись удалена!')
    await call.answer()
    await state.clear()


@router_delete.callback_query(DeleteUser.confirm, F.data == 'cancel_delete')
async def delete_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Удаление отменено.')
    await call.answer()
    await state.clear()