from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from db import main_db

router_fsm = Router()


class Registration(StatesGroup):
    name = State()
    age = State()
    phone = State()


@router_fsm.message(Command('cancel'))
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Анкета не заполнена.')
        return
    await state.clear()
    await message.answer('Заполнение анкеты отменено.')


@router_fsm.message(Command('form'))
async def start_form(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Registration.name)
    await message.answer('Как вас зовут?')


@router_fsm.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    name = (message.text or "").strip()
    if not name:
        await message.answer('Имя не может быть пустым. Введите ваше имя:')
        return
    await state.update_data(name=name)
    await state.set_state(Registration.age)
    await message.answer('Сколько вам лет?')


@router_fsm.message(Registration.age)
async def process_age(message: types.Message, state: FSMContext):
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer('Возраст должен быть числом! Попробуйте еще раз:')
        return
    await state.update_data(age=int(text))
    await state.set_state(Registration.phone)
    await message.answer('Введите ваш номер телефона:')


@router_fsm.message(Registration.phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone = (message.text or "").strip()
    if not phone:
        await message.answer('Номер телефона не может быть пустым. Введите номер еще раз:')
        return

    data = await state.get_data()
    data.update({'phone': phone})

    try:
        main_db.save_user({
            'name': data['name'],
            'age': int(data['age']),
            'phone': data['phone']
        })
    except Exception:
        await message.answer('Ошибка при сохранении, попробуйте позже.')
        await state.clear()
        return

    await state.clear()
    await message.answer(
        f"Заявка принята!\n\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Телефон: {data['phone']}"
    )