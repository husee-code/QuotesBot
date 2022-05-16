import json
import Levenshtein

with open('golden_quotes.json', encoding='utf-8') as js:
    golden_quotes = json.load(js)

teachers = golden_quotes.keys()


def removeBrackets(string:str):
    return string[:string.index('[')] + string[string.index('|')+1:string.index(']')] + string[string.index(']') + 1:]


def findTeacher(l: list, obj: str):
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


def f(d: dict):
    keys = d.keys()
    for i in keys:
        for j in keys:
            if 0 < Levenshtein.distance(i, j) < 5:
                d[i].extend(d[j])
                del d[j]
                return f(d)
    return d


edited_quotes = f(golden_quotes)
edited_quotes['Молодцова Ольга Викторовна'] = edited_quotes.pop('Молодцова Ольга викторовна')

edited_quotes["Заровский Анатолий Георгиевич"].extend(edited_quotes.pop("Заровский Анатолий Григорьевич"))

if "Базуева Ирина Игоревна" not in edited_quotes:
    edited_quotes["Базуева Ирина Игоревна"] = edited_quotes.pop("Базуеве Ирина Игоревна")

for teacher in edited_quotes.keys():
    for quote in edited_quotes[teacher]:
        if '|' in quote and '[' in quote:
            new_quote = removeBrackets(quote)
            edited_quotes[teacher].remove(quote)
            edited_quotes[teacher].append(new_quote)

with open('edited_quotes.json', 'w', encoding='utf-8') as js:
    json.dump(edited_quotes, js, ensure_ascii=False, sort_keys=True, indent=4)
