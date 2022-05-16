import os
import Levenshtein

vk_token = os.getenv('VK_TOKEN')


def findTeacher(l: list, obj: str) -> list[str] | bool:
    """
    Выполняет поиск по учителя среди данного списка
        :param l: Список, в котором ищем учителя
        :param obj: Строка с именем учителя для поиска
        :return: 10 наиболее похожих учителей. Если таковых не нашлось, False
    """

    obj = obj.lower()
    result = set()
    buttons = []

    if len(obj) < 3:
        print('меньше 3')
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
            buttons.append(i)
        return buttons[:10]
    return False


def mergeTwinKeys(d: dict):
    # Обьединяем похожие ключи
    keys = d.keys()
    for i in keys:
        for j in keys:
            if 0 < Levenshtein.distance(i, j) < 5:
                d[i].extend(d[j])
                del d[j]
                return mergeTwinKeys(d)
    return d


def mergeWithInvalidKeys(d: dict):
    # Избавляемся от ошибок
    d['Молодцова Ольга Викторовна'] = d.pop('Молодцова Ольга викторовна')

    d["Заровский Анатолий Георгиевич"].extend(d.pop("Заровский Анатолий Григорьевич"))

    if "Базуева Ирина Игоревна" not in d:
        d["Базуева Ирина Игоревна"] = d.pop("Базуеве Ирина Игоревна")

    return d


def removeBrackets(string: str):
    return string[:string.index('[')] + string[string.index('|') + 1:string.index(']')] + string[string.index(']') + 1:]


def removeLinks(d: dict):
    # Удаляем ссылки на людей из цитат
    for teacher in d.keys():
        for quote in d[teacher]:
            if '|' in quote and '[' in quote:
                new_quote = removeBrackets(quote)
                d[teacher].remove(quote)
                d[teacher].append(new_quote)
    return d


def fixDict(d: dict):
    """
    Убирает из словаря похожие ключи + исправляет ошибки (mergeWithInvalidKeys)
        :param d: словарь, который нужно исправить
        :return: исправленный словарь
    """

    step1 = mergeTwinKeys(d)
    step2 = mergeWithInvalidKeys(step1)
    step3 = removeLinks(step2)
    return step3
