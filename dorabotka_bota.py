from imghdr import tests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fail import *





api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text="Купить")
kb.row(button_1)
kb.row(button_2)
kb.add(button_3)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
i_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
i_button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.add(i_button_1)
kb2.add(i_button_2)

kb3 = InlineKeyboardMarkup(resize_keyboard=True) #
i_button_3 = InlineKeyboardButton(text="Продукт 1",callback_data="product_buying")
i_button_4 = InlineKeyboardButton(text="Продукт 2",callback_data="product_buying")
i_button_5 = InlineKeyboardButton(text="Продукт 3",callback_data="product_buying")
i_button_6 = InlineKeyboardButton(text="Продукт 4",callback_data="product_buying")

kb3.add(i_button_3)
kb3.row(i_button_4)
kb3.row(i_button_5)
kb3.row(i_button_6)

class UserState(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


@dp.message_handler(commands=['start'])
async def starts(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.',reply_markup=kb)


@dp.message_handler(text="Информация")
async def info(message):
    await message.answer("Я бот помогающий твоему здоровью,Если хотите рассчитать вашу "
                         "норму калорий - нажмите кнопку Рассчитать")


@dp.message_handler(text='рассчитать')
async def menu(message):
    await message.answer('Выберите опцию:',reply_markup=kb2)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norm_calories_men = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    norm_calories_vomen = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f"Мужская норма в сутки {norm_calories_men} ккал."
                         f" Женская норма в сутки {norm_calories_vomen} ккал.")
    await state.finish()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in range(4):
        number = i + 1
        await message.answer(f"Название: Product {number} | Описание: описание {number} | Цена: {number*100}")
        with open(f'fail/{str(number)}kartinki.pip.jpg','rb') as img:
            await message.answer_photo(img)

        await message.answer(text='Выберете продукт для покупки:',reply_markup=kb3)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer(text="Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')
# Упрощенный вариант формулы Миффлина - Сан Жеора:
# для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
# для женщин: 10 х вес (кг) + 6,25 х рост (см) - 5 х возраст (г) -161

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

'''
from aiogram import Bot, Dispatcher,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# ------ Маркап клавиатура (с кнопками)----------------
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button3 = KeyboardButton(text='Купить')
kb.row(button)
kb.row(button2)
kb.add(button3)

#-------- Инлайн клавиатуры (с кнопками)----------------
kb2 = InlineKeyboardMarkup()
in_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

kb2.add(in_button1)
kb2.add(in_button2)
kb3 = InlineKeyboardMarkup(resize_keyboard=True) # покупка продукта

in_button3 = InlineKeyboardButton(text='Продукт1', callback_data='product_buying')
in_button4 = InlineKeyboardButton(text='Продукт2', callback_data='product_buying')
in_button5 = InlineKeyboardButton(text='Продукт3', callback_data='product_buying')
in_button6 = InlineKeyboardButton(text='Продукт4', callback_data='product_buying')

kb3.add(in_button3)
kb3.row(in_button4)
kb3.row(in_button5)
kb3.row(in_button6)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('На текущий момент я пока только могу рассчитать необходимое количество килокалорий (ккал) '
                         'в сутки для каждого конкретного человека. \n По формулуe Миффлина-Сан Жеора, разработанной '
                         'группой американских врачей-диетологов под руководством докторов Миффлина и Сан Жеора. \n'
                         'Погнали!? - жми кнопку Рассчитать')

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              '\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Данные необходимо вводить целыми числами')
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    mans = (10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])+5)
    wumans = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f'При таких параметрах норма калорий: \nдля мужчин {mans} ккал в сутки \nдля женщин {wumans} ккал в сутки')
    await UserState.weight.set()
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(4):
        number = i + 1
        await message.answer(f'Название: Product{number} | Описание: описание{number} | Цена: {number*100}')
        with open (f'{str(number) + ".png"}', 'rb') as img:
            await message.answer_photo(img)

    await message.answer(text='Выберите продукт для покупки: ', reply_markup=kb3)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler()
async def all_message(message):
   await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
'''









'''
Создайте и дополните клавиатуры:
В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3",
 "Product4". У всех кнопок назначьте callback_data="product_buying"
Создайте хэндлеры и функции к ним:
Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию
get_buying_list(message).
Функция get_buying_list должна выводить надписи 'Название: Product<number> |
Описание: описание <number> | Цена: <number * 100>' 4 раза. После каждой надписи
выводите картинки к продуктам. В конце выведите ранее созданное Inline меню с
надписью "Выберите продукт для покупки:".
Callback хэндлер, который реагирует на текст "product_buying" и оборачивает
функцию send_confirm_message(call).
Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"
'''
