import re
from typing import List

from api import ApiWrapper

class RevsWithTypes:

    def __init__(self, lang: str, site_name: str, title: str):
        self.lang = lang
        self.site_name = site_name
        self.title = title
        
    def convert_revisions_to_list():
        api_wrapper = ApiWrapper(self.lang, self.site_name)
        revisions = api_wrapper.get_revisions_diffs(self.title)
        converted = list(map(
        lambda x: {
            'old_revid': x.old_revid,
            'new_revid': x.new_revid,
            'lines_diffs': list(map(lambda diff: {'old': diff[0], 'new': diff[1]}, x.lines_diffs))
        },
        revisions))
        return converted
     
    def add_type_to_revision():
        revisions = convert_revisions_to_list()
        links_regex = 'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        wiki_links_regex = 'http[s]?:\/\/(?:[a-zA-Z])+.wikipedia.org\/'
        for dict in revisions:
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
        return revisions