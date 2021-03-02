import re
from add_type import RevsWithTypes
import json

if __name__ == '__main__':
    api_wrapper = RevsWithTypes('ru', 'wikipedia', 'Пермский_национальный_исследовательский_политехнический_университет')
    revisions = api_wrapper.add_type_to_revision()
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(revisions, f, ensure_ascii=False)
