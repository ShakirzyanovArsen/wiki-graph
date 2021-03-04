import re

class RevsWithTypes:

    def __init__(self):
        pass
        
    def convert_revisions_to_list(self, revisions):
        converted = list(map(
        lambda x: {
            'old_revid': x.old_revid,
            'new_revid': x.new_revid,
            'lines_diffs': list(map(lambda diff: {'old': diff[0], 'new': diff[1]}, x.lines_diffs))
        },
        revisions))
        return converted
     
    def add_type_to_revision(self, revisions):
        revisions_list = self.convert_revisions_to_list(revisions)
        links_regex = 'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        wiki_links_regex = 'http[s]?:\/\/(?:[a-zA-Z])+.wikipedia.org\/'
        for dict in revisions_list:
            lines_diffs_list = dict['lines_diffs']
            for line_numb in range(len(lines_diffs_list)):
                line_diffs = lines_diffs_list[line_numb]
                if line_diffs['new'] is None:
                    line_diffs['type'] = 'Малая правка'
                else:
                    match_link = re.search(links_regex, line_diffs['new'], flags=re.IGNORECASE)
                    if match_link:
                        match_wiki_link = re.search(wiki_links_regex, line_diffs['new'], flags=re.IGNORECASE)
                        if match_wiki_link:
                            line_diffs['type'] = 'Перевод вики-страницы'
                        else:
                            line_diffs['type'] = 'Ссылка на источник'
                    else:
                        line_diffs['type'] = 'Малая правка'
        return revisions_list