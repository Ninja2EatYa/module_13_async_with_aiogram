from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
import asyncio

api = '7128421160:AAH1J2WSK_MvAnq3ugj1jAFnRuphTehiveM'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.insert(button_1)
kb.insert(button_2)
kb.resize_keyboard = True



class UserState(StatesGroup):
    male = True
    age = State()
    height = State()
    weight = State()


@dp.message_handler(commands='START')
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!\n\nНажмите /Рассчитать, чтобы посчитать '
                         'необходимое вам суточное количество калорий', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Нажмите /START, чтобы начать общение.')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.height.set()


@dp.message_handler(state=UserState.height)
async def set_weight(message, state):
    await state.update_data(height=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if UserState.male:
        calories = f'{(10 * float(data["weight"]) + 6.25 * float(data["height"]) - 5 * float(data["age"]) + 5) * 1.55}'
    else:
        calories = f'{(10 * float(data["weight"]) + 6.25 * float(data["height"]) - 5 * float(data["age"]) - 161) * 1.55}'
    await message.answer(f'Необходимое вам количество килокалорий в сутки составляет {round(float(calories), 2)} (ккал)')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
