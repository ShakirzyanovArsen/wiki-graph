import re
from datetime import datetime

import pywikibot
from pywikibot.diff import Hunk, PatchManager
from pywikibot.page import Revision
from typing import List

from add_type import RevsWithTypes


class RevisionDiff:
    def __init__(self, old_revid: int, new_revid: int, old_ts: datetime, new_ts: datetime, lines_diffs: List[tuple]):
        self.old_revid = old_revid
        self.new_revid = new_revid
        self.old_ts = old_ts
        self.new_ts = new_ts
        # each element is tuple where fist element of tuple is old string, second - new string
        # if string is added at end of paragraph, then first element - None
        self.lines_diffs = lines_diffs
        pass

    @staticmethod
    def of_hunks(
            old_revid: int,
            new_revid: int,
            old_ts: pywikibot.Timestamp,
            new_ts: pywikibot.Timestamp,
            hunks: List[Hunk]):

        lines_diffs = []

        def convert_str(s: str):
            remove_start_sign = re.sub(r"^[-+][ \n]+", '', s)
            if len(remove_start_sign) == 0:
                return None
            return remove_start_sign

        for h in hunks:
            hunk_diff = h.diff
            if len(hunk_diff) == 1:
                lines_diffs.append((None, convert_str(hunk_diff[0])))
            else:
                lines_diffs.append((convert_str(hunk_diff[0]), convert_str(hunk_diff[len(hunk_diff) - 1])))
        return RevisionDiff(
            old_revid,
            new_revid,
            old_ts,
            new_ts,
            lines_diffs)

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                map(lambda x: "'{}' -> '{}'".format(x[0], x[1]), self.lines_diffs)
            ).replace("\n", "\\n")
        )

    def __eq__(self, o: object) -> bool:
        if type(o) is type(self):
            return self.__dict__ == o.__dict__
        return False


class ApiWrapper:

    def __init__(self, lang: str, site_name: str):
        self.site = pywikibot.Site(lang, site_name)

    def get_revisions_diffs(self, title: str) -> List[RevisionDiff]:
        page = pywikibot.Page(self.site, title)
        revisions = page.revisions(content=True)
        result = []
        for revision in revisions:
            result.append(revision)
        return self._convert_revisions_to_diffs(result)

    @staticmethod
    def _convert_revisions_to_diffs(revisions: List[Revision]) -> List[RevisionDiff]:
        if len(revisions) <= 1:
            return []
        result = []
        revisions.sort(key=lambda val: val.timestamp)
        for i in range(1, len(revisions)):
            old_rev = revisions[i - 1]
            new_rev = revisions[i]
            pm = PatchManager(old_rev.slots['main']['*'], new_rev.slots['main']['*'])
            rev_diff = RevisionDiff.of_hunks(
                revisions[i - 1].revid,
                revisions[i].revid,
                revisions[i - 1].timestamp,
                revisions[i].timestamp,
                pm.hunks
            )
            result.append(rev_diff)
        add_type = RevsWithTypes()
        result = add_type.add_type_to_revision(result)
        return result
