from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

key_api = '7663863093:AAHBqmiFkF15GWjTPKjsmgb68wyN-Iz8QVg'
bot = Bot(token=key_api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button_age = KeyboardButton(text = 'Рассчитать')
button_info = KeyboardButton(text = 'Информация')
kb.add(button_age, button_info)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def keyboard_add(message):
    await message.answer("Этот бот подсчитывает калории, чтобы активировать, нажмите на кнопку 'Рассчитать'", reply_markup = kb)

@dp.message_handler(text = "Рассчитать")
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(first = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(second = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(third = message.text)
    data = await state.get_data()
    bmr = 10 * float(data['third']) + 6.25 * float(data['second']) - 5 * float(data['first']) + 5
    await message.answer(f"Ваша норма калорий: {bmr}")
    await state.finish()

@dp.message_handler()
async def start(message):
    await message.answer("Привет! Чтобы начать, чтобы меня активировать нужна команда /start")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)