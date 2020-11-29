from api import ApiWrapper
import json

if __name__ == '__main__':
    api_wrapper = ApiWrapper('ru', 'wikipedia')
    revisions = api_wrapper.get_revisions_diffs('Пермский_национальный_исследовательский_политехнический_университет')
    converted = list(map(
        lambda x: {
            'old_revid': x.old_revid,
            'new_revid': x.new_revid,
            'lines_diffs': list(map(lambda diff: {'old': diff[0], 'new': diff[1]}, x.lines_diffs))
        },
        revisions))
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(converted, f, ensure_ascii=False)
