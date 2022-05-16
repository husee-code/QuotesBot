from __future__ import annotations
import random
import Levenshtein
import requests
from aiogram.types import InlineKeyboardButton
from colorama import Fore

from keyboards import none_button, next_page_button, previous_page_button, back_button
from .utils import vk_token
from .vars import all_quotes_dict, teachers, group_id


async def checkNewQuoteVK(bot, last_quote=None):
    """
        Проверяем группу ВК на наличие новой цитаты. Если такая имеется, добавляем в словарь all_quotes_dict

            :param bot: Объект бота TG
            :param last_quote: Последняя цитата в паблике ВК
    """

    response = requests.get(
        f'https://api.vk.com/method/wall.get?domain=zolotoicitatnik&count=1&access_token={vk_token}&v=5.131').json()
    quote = response['response']['items'][0]['text']

    # Если нашли новую цитату:
    if '@' in quote and quote != last_quote:
        quote_text = quote.split('@')[::-1]  # Переворачиваем, чтобы передать список [учитель, цитата]
        print(Fore.GREEN + f'Найдена новая цитата из группы ВК: \n ' +
              Fore.RESET + f'{quote_text[1]}\n@{quote_text[0]}')
        await addQuote(quote_text)
        await submitToTG(quote_text, bot=bot)
        # TODO Функция, обновляющая last_quote
        # last_quote = quote

    else:
        print(Fore.RED + 'Новых цитат в группе ВК не найдено.' + Fore.RESET)


# В качестве исходного словаря с цитатами используется all_quotes_dict
async def randomQuote():
    random_teacher = random.choice(teachers)
    quote = random.choice(all_quotes_dict[random_teacher])
    return f'{quote}\n@{random_teacher}'


async def teacherQuote(teacher):
    random_quote = random.choice(all_quotes_dict[teacher])
    return f'{random_quote}\n@{teacher}'


def getTeachers(iterable, page_number=1):
    l = len(iterable)
    pages = l // 10 if l % 10 == 0 else l // 10 + 1
    # Если находимся на первой странице:
    if page_number == 1:
        # Если есть еще страницы:
        if l > 10:
            for teacher in iterable[:10]:
                yield InlineKeyboardButton(text=teacher, callback_data=teacher)
            yield none_button
            yield next_page_button
        # Если всего только одна страница:
        else:
            for teacher in iterable:
                yield InlineKeyboardButton(text=teacher, callback_data=teacher)
    # Если находимся не на последней странице:
    elif page_number < pages:
        for teacher in iterable[(page_number - 1) * 10 + 1:10 * page_number + 1]:
            yield InlineKeyboardButton(text=teacher, callback_data=teacher)
        yield previous_page_button
        yield next_page_button
    # Если на последней странице:
    elif page_number == pages:
        for teacher in iterable[(page_number - 1) * 10 + 1:10 * page_number + 1]:
            yield InlineKeyboardButton(text=teacher, callback_data=teacher)

        if l % 2 == 0:
            yield none_button
            yield previous_page_button
        else:
            yield none_button
            yield none_button
            yield previous_page_button
    yield back_button


async def allQuotes(teacher):
    v = ''
    for quote in all_quotes_dict[teacher]:
        v += quote + '\n'
    return v


async def findTeacher(l: list, obj: str):
    obj = obj.lower()
    result = set()
    buttons = []

    if len(obj) < 3:
        for teacher in l:
            if teacher.lower().startswith(obj):
                result.add(teacher)
    else:
        for teacher in l:
            if obj in teacher.lower():
                result.add(teacher)
        for teacher in l:
            if 0 < Levenshtein.distance(obj.lower(), teacher.split()[0]) <= 2:
                result.add(teacher)

    if result:
        for i in result:
            buttons.append(InlineKeyboardButton(text=i, callback_data=i))
        return buttons[:10]
    return False


async def addQuote(quote: list | tuple):
    """
            Добавляет в словарь all_quotes_dict новую цитату

            :param quote: Список или кортеж (Учитель, цитата)
    """

    teacher = quote[0]
    quote_text = quote[1]

    if teacher in all_quotes_dict:
        all_quotes_dict[teacher].append(quote_text + '\n')
    else:
        all_quotes_dict[teacher] = [quote_text + '\n']


async def submitToTG(quote: list | tuple, bot):
    """
        Выкладывает цитату учителя в телеграм канал.

            :param quote: Список или кортеж (Учитель, цитата)
            :param bot: Объект бота TG
    """

    # Опубликовываем цитату в телеграм канал
    await bot.send_message(chat_id=group_id, text=f'{quote[1]}\n@{quote[0]}')
