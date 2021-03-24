from api import ApiWrapper
from add_type import RevsWithTypes
from graph import MakeGraph
import json

if __name__ == '__main__':
    page_name = 'Пермский_национальный_исследовательский_политехнический_университет'
    api_wrapper = ApiWrapper('ru', 'wikipedia')
    revisions = api_wrapper.get_revisions_diffs(page_name)
    add_type = RevsWithTypes()
    result = add_type.add_type_to_revision(revisions)
    make_graph = MakeGraph()
    graph = make_graph.make_graph(result, page_name)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False)
