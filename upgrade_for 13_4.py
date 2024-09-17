from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()
    sex = ''


@dp.message_handler(commands='START')
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!')
    await message.answer('Нажмите /CALORIES, чтобы посчитать необходимое вам суточное количество калорий')


@dp.message_handler(commands='CALORIES')
async def set_sex(message):
    await message.answer('Выберите свой пол : /MALE or /FEMALE')


@dp.message_handler(commands='MALE')
async def set_age(message):
    UserState.sex = 'male'
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(commands='FEMALE')
async def set_age(message):
    UserState.sex = 'female'
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
    if UserState.sex == 'male':
        calories = f'{(10 * float(data["weight"]) + 6.25 * float(data["height"]) - 5 * float(data["age"]) + 5) * 1.55}'
    else:
        calories = f'{(10 * float(data["weight"]) + 6.25 * float(data["height"]) - 5 * float(data["age"]) - 161) * 1.55}'
    await message.answer(f'Необходимое вам количество килокалорий в сутки составляет {round(float(calories), 2)} (ккал)')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
