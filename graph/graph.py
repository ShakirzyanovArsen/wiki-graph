class MakeGraph:

    def __init__(self):
        pass

    def make_graph(self, revisions, reviewed_page):
        graph = {'vertices': [], 'edges': []}
        vertices = []
        vertices.append(reviewed_page)
        for dict in revisions:
            lines_diffs_list = dict['lines_diffs']
            for line_numb in range(len(lines_diffs_list)):
                line_diffs = lines_diffs_list[line_numb]
                if line_diffs['type'] == 'Малая правка':
                    edge = {'from': reviewed_page, 'to': reviewed_page, 'weight': line_diffs['type'], 'new': line_diffs['new']}
                    graph['edges'].append(edge)
                if line_diffs['type'] == 'Ссылка на источник' or line_diffs['type'] == 'Перевод вики-страницы':
                    edge = {'from': reviewed_page, 'to': line_diffs['new'], 'weight': line_diffs['type']}
                    graph['edges'].append(edge)
                    vertices.append(line_diffs['new'])
        vertices = list(dict.fromkeys(vertices))
        graph['vertices'] = vertices
        return graph