from api import ApiWrapper
import json

if __name__ == '__main__':
    api_wrapper = ApiWrapper('ru', 'wikipedia')
    revisions = api_wrapper.get_revisions_diffs('Пермский_национальный_исследовательский_политехнический_университет')
    print(revisions[0])
