from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import asyncio

api = '7128421160:AAF8Yqk5pJpUMG14ppowz4ojPuGSzI8lV10'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]
    ], resize_keyboard=True
)


inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)


class UserState(StatesGroup):
    male = True
    age = State()
    height = State()
    weight = State()


@dp.message_handler(commands='START')
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!\n\nНажми &#128073; Рассчитать &#128072;, чтобы посчитать '
                         'необходимое тебе суточное количество калорий', reply_markup=kb, parse_mode='HTML')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выбери опцию: &#128071;', reply_markup=inline_menu, parse_mode='HTML')


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('&#9888; Формула Миффлина-Сан Жеора, учитывающая степень физической активности человека:\n\n'
                               '<b><u>Для мужчин:</u></b>\n(10 &#215; вес (кг) + 6.25 &#215; рост (см) – 5 &#215; возраст (г) + 5) &#215; A\n'
                               '<b><u>Для женщин:</u></b>\n(10 &#215; вес (кг) + 6.25 &#215; рост (см) – 5 &#215; возраст (г) – 161) &#215; A\n\n'
                               '<i>где A – это уровень активности человека.\nЗдесь принят коэффициент средней активности A = 1,55.</i>', parse_mode='HTML')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def get_calories(call):
    await call.message.answer('&#11093; Введи свой возраст:', parse_mode='HTML')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(text='Информация')
async def all_massages(message):
    await message.answer('&#169; <b><i>Ninja2EatYa</i></b>, 2024', parse_mode='HTML')


@dp.message_handler()
async def all_massages(message):
    await message.answer('Начнем заново?\n\nНажми &#128073; /START &#128072;', parse_mode='HTML')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('&#11093; Введи свой рост:', parse_mode='HTML')
    await UserState.height.set()


@dp.message_handler(state=UserState.height)
async def set_weight(message, state):
    await state.update_data(height=message.text)
    await message.answer('&#11093; Введи свой вес:', parse_mode='HTML')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if UserState.male:
        calories = f'{(10 * float(data["weight"]) + 6.25 * float(data["height"]) - 5 * float(data["age"]) + 5) * 1.55}'
    else:
        calories = f'{(10 * float(data["weight"]) + 6.25 * float(data["height"]) - 5 * float(data["age"]) - 161) * 1.55}'
    await message.answer(
        f'Необходимое тебе количество килокалорий в сутки составляет:\n&#128073; {round(float(calories), 2)} (ккал) &#128072;', parse_mode='HTML')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
