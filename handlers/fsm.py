from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router_fsm = Router()

@router_fsm.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Анкета не заполнена.')
    else:
        await state.clear()
        await message.answer('Заполнение анкеты отменено.')

class Registration(StatesGroup):
    name = State()
    age = State()
    phone = State()

@router_fsm.message(Command('form'))
async def start_form(message: Message, state: FSMContext):
    await message.answer('Как вас зовут?')
    await state.set_state(Registration.name)

@router_fsm.message(Registration.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Сколько вам лет?')
    await state.set_state(Registration.age)

@router_fsm.message(Registration.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Возраст должен быть числом! Попробуйте еще раз:')
        return 
    await state.update_data(age=int(message.text))
    await message.answer('Введите ваш номер телефона: ')
    await state.set_state(Registration.phone)

@router_fsm.message(Registration.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await message.answer(
    f"Заявка принята!\n\n"
    f"Имя: {data['name']}\n"
    f"Возраст: {data['age']}\n"
    f"Телефон: {data['phone']}"
)
    await state.clear()
    await state.clear()


class AddProduct(StatesGroup):
    name = State()
    price = State()
    description = State()

@router_fsm.message(Command('add_product'))
async def add_start_fsm(message: Message, state: FSMContext):
    await message.answer('Введите название товара:')
    await state.set_state(AddProduct.name)

@router_fsm.message(AddProduct.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите цену товара')
    await state.set_state(AddProduct.price)

@router_fsm.message(AddProduct.price)
async def add_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Цена должна быть числом. Попробуйте еще раз')
    else:
        await state.update_data(price=message.text)
        await message.answer('Введите описание для данного товара:')
        await state.set_state(AddProduct.description)

@router_fsm.message(AddProduct.description)
async def add_description(message: Message, state: FSMContext):
    data = await state.update_data(description=message.text)

    await message.answer(
        f"Товар добавлен!\n"
        f"Название товара - {data['name']}\n"
        f"Цена: {data['price']}\n"
        f"Описание: {data['description']}"
    )

    await state.clear()