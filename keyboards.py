from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_text = 'Дарова, это тг бот золотого цитатника.' \
             'Чтобы перейти в инлайн режим, пиши /inline \n' \
             'Поиск по учителям работает, пиши и не сы\n' \

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
back_button = InlineKeyboardButton(text="Назад", callback_data="back")

inline_start_commands = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Случайная цитата', callback_data='random_quote'),
    InlineKeyboardButton(text='Список учителей', callback_data='teachers_list'),
    InlineKeyboardButton(text='Предложить цитату', callback_data='suggest'),
)
inline_choose_option = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Случайная цитата', callback_data='random_quote'),
    InlineKeyboardButton(text='Все цитаты', callback_data='all_quotes'),
    back_button

)
start_commands = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True).add(
    KeyboardButton(text='Случайная цитата'),
    KeyboardButton(text='Список учителей'),
    KeyboardButton(text='Предложить цитату')
)

next_page_button = InlineKeyboardButton(text="➡️", callback_data="np")
previous_page_button = InlineKeyboardButton(text="⬅️", callback_data="bp")
none_button = InlineKeyboardButton(text="", callback_data="None")

# админ панелька

ap_start = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text='Проверить предложку', callback_data='check'),

)

ap_check_quote = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text='Изменить ФИО', callback_data='change_fio'),
    InlineKeyboardButton(text='Изменить цитату', callback_data='change_quote'),
    InlineKeyboardButton(text='Опубликовать', callback_data='submit'),
    InlineKeyboardButton(text='Отклонить', callback_data='reject'),
)
