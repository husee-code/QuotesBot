import json

page_dict = {}
input_quotes_list: list = []
admins: tuple[int, int] = (347249536, 714799964)
new_quote = []
group_id = -1001513445928
last_quote: str = '"Да тут рампапам конкретный!"\n@Терехина Елена Владимировна'

# Собираем цитаты
with open('edited_quotes.json', encoding='utf-8') as js:
    all_quotes_dict = json.load(js)

teachers = [i for i in all_quotes_dict.keys()]  # Все учителя