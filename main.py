from api import ApiWrapper
from add_type import RevsWithTypes
import json

if __name__ == '__main__':
    api_wrapper = ApiWrapper('ru', 'wikipedia')
    revisions = api_wrapper.get_revisions_diffs('Пермский_национальный_исследовательский_политехнический_университет')
    add_type = RevsWithTypes()
    result = add_type.add_type_to_revision(revisions)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)
