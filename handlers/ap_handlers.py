from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards import ap_check_quote, ap_start
from utils.functions import addQuote, submitToTG
from utils.vars import *

new_quote = []


class AdminStates(StatesGroup):
    AP_START_STATE = State()
    AP_CHECK_QUOTE_STATE = State()

    AP_CHANGE_FIO_STATE = State()
    AP_CHANGE_QUOTE_STATE = State()


def register_ap_handlers(dp, bot):
    # Админ панелька здесь
    @dp.callback_query_handler(state=AdminStates.AP_START_STATE)
    async def apStartCommands(cmd: types.CallbackQuery):
        global new_quote

        match cmd.data:
            case 'check':
                if len(input_quotes_list):
                    await cmd.answer(f'Цитат на проверку в очереди: {len(input_quotes_list)}')
                    new_quote = input_quotes_list.pop(0)
                    await cmd.message.answer(text=f'*ФИО*:\n```\n{new_quote[0]}```\n'
                                                  f'*Цитата*:\n```\n{new_quote[1]}```',
                                             reply_markup=ap_check_quote, parse_mode='Markdown')
                    await AdminStates.AP_CHECK_QUOTE_STATE.set()
                else:
                    await cmd.answer('Цитат на проверку нет и слава богу')

    # Проверка цитаты
    @dp.callback_query_handler(state=AdminStates.AP_CHECK_QUOTE_STATE)
    async def checkQuote(callback: types.CallbackQuery):
        match callback.data:
            case 'change_fio':
                await callback.message.answer(text='Введите правильное ФИО')
                await AdminStates.AP_CHANGE_FIO_STATE.set()
                # ХЕНДЛЕР НИЖЕ

            case 'change_quote':
                await callback.message.answer(text='Отправьте цитату с исправленными ошибками')
                await AdminStates.AP_CHANGE_QUOTE_STATE.set()
                # ХЕНДЛЕР НИЖЕ

            case 'submit':
                await addQuote(new_quote)
                await callback.message.answer(text='Цитата добавлена!', reply_markup=ap_start)
                await submitToTG(new_quote, bot)
                await AdminStates.AP_START_STATE.set()

            case 'reject':
                await callback.message.answer(text='Цитата отклонена.', reply_markup=ap_start)
                await AdminStates.AP_START_STATE.set()

    # Изменение ФИО в цитате на проверку
    @dp.message_handler(state=AdminStates.AP_CHANGE_FIO_STATE)
    async def changeFIO(fio: types.Message):
        global new_quote
        new_quote = (fio.text, new_quote[1])
        await fio.answer(text=f'*ФИО*:\n```\n{new_quote[0]}```\n'
                              f'*Цитата*:\n```\n{new_quote[1]}```',
                         reply_markup=ap_check_quote, parse_mode='Markdown')
        await AdminStates.AP_CHECK_QUOTE_STATE.set()

    # Изменение текста цитаты в цитате на проверку
    @dp.message_handler(state=AdminStates.AP_CHANGE_QUOTE_STATE)
    async def changeQuote(quote: types.Message):
        global new_quote
        new_quote = (new_quote[0], quote.text)
        await quote.answer(text=f'*ФИО*:\n```\n{new_quote[0]}```\n'
                                f'*Цитата*:\n```\n{new_quote[1]}```',
                           reply_markup=ap_check_quote, parse_mode='Markdown')
        await AdminStates.AP_CHECK_QUOTE_STATE.set()
