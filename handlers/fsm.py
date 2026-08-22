from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from db import main_db

router_fsm = Router()


class Registration(StatesGroup):
    name = State()
    age = State()
    phone = State()
    photo = State()
    city = State()


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
    await state.update_data(phone=phone)
    await state.set_state(Registration.photo)
    await message.answer('Отправьте ваше фото:')


@router_fsm.message(Registration.photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await state.set_state(Registration.city)
    await message.answer('Из какого вы города?')


@router_fsm.message(Registration.photo)
async def process_photo_invalid(message: types.Message):
    await message.answer('Отправьте именно фото.')


@router_fsm.message(Registration.city)
async def process_city(message: types.Message, state: FSMContext):
    city = (message.text or "").strip()
    if not city:
        await message.answer('Город не может быть пустым. Введите город еще раз:')
        return

    data = await state.get_data()
    data.update({'city': city})

    try:
        user_id = await main_db.save_user({
            'name': data['name'],
            'age': int(data['age']),
            'phone': data['phone'],
            'photo_id': data['photo_id']
        })
        await main_db.save_user_info(user_id, {'city': data['city']})
    except Exception:
        await message.answer('Ошибка при сохранении.')
        await state.clear()
        return

    await state.clear()
    await message.answer_photo(
        photo=data['photo_id'],
        caption=(
            f"Заявка принята!\n\n"
            f"Имя: {data['name']}\n"
            f"Возраст: {data['age']}\n"
            f"Телефон: {data['phone']}\n"
            f"Город: {data['city']}"
        )
    )