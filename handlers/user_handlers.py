from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup

from handlers.ap_handlers import AdminStates
from keyboards import ap_start, start_text, start_commands, inline_choose_option
from utils.functions import randomQuote, getTeachers, teacherQuote, allQuotes
from utils.utils import findTeacher
from utils.vars import teachers, admins, input_quotes_list, page_dict

teachers = teachers


class UserStates(StatesGroup):
    START_STATE = State()
    TEACHERS_LIST_STATE = State()
    CHOOSE_OPTION_STATE = State()
    FIO_INPUT_STATE = State()
    QUOTE_INPUT_STATE = State()


def register_user_handlers(dp, bot):
    @dp.message_handler(commands=['start', 'help', 'open_panel'], state='*')
    async def start(message: types.Message):
        await UserStates.START_STATE.set()
        match message.text:
            case '/open_panel':
                if message.chat.id in admins:
                    await message.answer('Открываю админ панельку', reply_markup=ap_start)
                    await AdminStates.AP_START_STATE.set()
                else:
                    await message.answer('Пошел нахуй')
            case _:
                await message.answer(start_text, reply_markup=start_commands)

    # Предложка пошлаа
    # Ввод ФИО учителя
    @dp.message_handler(state=UserStates.FIO_INPUT_STATE)
    async def FIO_input(fio: types.Message, state: FSMContext):
        await state.update_data(fio=fio.text)
        await fio.answer('Отлично! Теперь отправь цитату')
        await UserStates.QUOTE_INPUT_STATE.set()

    @dp.message_handler(state=UserStates.QUOTE_INPUT_STATE)
    async def quoteInput(quote: types.Message, state: FSMContext):
        await state.update_data(quote=quote.text)
        user_data = await state.get_data()
        input_quotes_list.append((user_data['fio'], user_data['quote']))
        await quote.answer('Цитата отправлена на проверку', reply_markup=start_commands)
        await UserStates.START_STATE.set()

    # Выбор: 'Случайная цитата', 'Список учителей', 'Предложить цитату'
    @dp.message_handler(state='*')
    async def start_buttons_check(message: types.Message):
        match message.text:
            case 'Случайная цитата':
                await message.answer(text=await randomQuote())
            case 'Список учителей':
                page_dict[message.chat.id] = 1
                await message.answer(text='Список учителей:', reply_markup=InlineKeyboardMarkup(row_width=2).add(
                    *getTeachers(iterable=teachers)
                ))
                await UserStates.TEACHERS_LIST_STATE.set()
            case 'Предложить цитату':
                await message.answer('Введи ФИО учителя (или хотя бы попытайся блядь)')
                await UserStates.FIO_INPUT_STATE.set()

            # Поиск учителя (ввод с клавиатуры)
            case _:
                result = findTeacher(teachers, message.text)
                if result:
                    await message.answer(text='Что-то нашлось:', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                        *result
                    ))
                    await UserStates.TEACHERS_LIST_STATE.set()
                else:
                    await message.answer(text='Ничего не нашлось. Попробуйте еще')

    # выбор учителя
    @dp.callback_query_handler(state=UserStates.TEACHERS_LIST_STATE)
    async def chooseTeacher(callback: types.CallbackQuery, state: FSMContext):
        match callback.data:
            case 'np':
                page_dict[callback.message.chat.id] += 1
                await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(row_width=2).add(
                    *getTeachers(iterable=teachers, page_number=page_dict[callback.message.chat.id])))
            case 'bp':
                page_dict[callback.message.chat.id] -= 1
                await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(row_width=2).add(
                    *getTeachers(iterable=teachers, page_number=page_dict[callback.message.chat.id])))
            case 'back':
                await callback.message.delete()
                await bot.send_message(chat_id=callback.message.chat.id,
                                       text=start_text, reply_markup=start_commands)
            case _:
                await callback.message.edit_text(text=callback.data, reply_markup=inline_choose_option)
                await state.update_data(teacher=callback.data)
                await UserStates.CHOOSE_OPTION_STATE.set()

    @dp.callback_query_handler(state=UserStates.CHOOSE_OPTION_STATE)
    async def inlineChooseOption(callback: types.CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        match callback.data:
            case 'random_quote':

                await callback.message.answer(text=await teacherQuote(teacher=user_data['teacher']),
                                              reply_markup=inline_choose_option)

            case 'all_quotes':
                await callback.message.answer(text=f'Все цитаты учителя {user_data["teacher"]}:')
                await callback.message.answer(text=await allQuotes(user_data["teacher"]))

    # INLINE Выбор: 'Случайная цитата', 'Список учителей', 'Предложить цитату'
    @dp.callback_query_handler(state=UserStates.START_STATE)
    async def inline_start_buttons(callback: types.CallbackQuery):
        match callback.data:
            case 'random_quote':
                await callback.message.answer(text=await randomQuote())
            case 'teachers_list':
                pass
            case 'suggest':
                pass
