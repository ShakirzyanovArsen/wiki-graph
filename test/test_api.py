import os
import unittest

os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'

from pywikibot import Timestamp
from pywikibot.page import Revision

from api import ApiWrapper, RevisionDiff, datetime


class TestApiWrapper(unittest.TestCase):

    def test_two_revisions(self):
        revisions = [
            Revision(1, Timestamp.fromtimestampformat('20200112'), 'test_user', slots={
                'main': {
                    'contentmodel': 'wikitext',
                    'contentformat': 'text/x-wiki',
                    '*': '[[Изображение:test.gif|thumb]]\n\nold\n\ntest test test\n\n'
                }
            }),
            Revision(2, Timestamp.fromtimestampformat('20200115'), 'test_user', slots={
                'main': {
                    'contentmodel': 'wikitext',
                    'contentformat': 'text/x-wiki',
                    '*': '[[Изображение:test.gif|thumb]]\n\ntest test test\n\nnewline\n'
                }
            })
        ]
        diffs = ApiWrapper._convert_revisions_to_diffs(revisions)
        self.assertEqual(1, len(diffs))
        self.assertEqual(RevisionDiff(
            old_ts=datetime.strptime('2020-01-12T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
            new_ts=datetime.strptime('2020-01-15T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
            old_revid=1,
            new_revid=2,
            lines_diffs=[(None, 'old\n'), (None, 'newline\n')]
        ), diffs[0])

    def test_empty_input(self):
        diffs = ApiWrapper._convert_revisions_to_diffs([])
        self.assertListEqual(diffs, [])

    def test_two_revisions_reverse_order(self):
        revisions_wrong_order = [
            Revision(2, Timestamp.fromtimestampformat('20200115'), 'test_user', slots={
                'main': {
                    'contentmodel': 'wikitext',
                    'contentformat': 'text/x-wiki',
                    '*': '[[Изображение:test.gif|thumb]]\n\ntest test test\n\nnewline\n'
                }
            }),
            Revision(1, Timestamp.fromtimestampformat('20200112'), 'test_user', slots={
                'main': {
                    'contentmodel': 'wikitext',
                    'contentformat': 'text/x-wiki',
                    '*': '[[Изображение:test.gif|thumb]]\n\nold\n\ntest test test\n\n'
                }
            })
        ]
        diffs = ApiWrapper._convert_revisions_to_diffs(revisions_wrong_order)
        self.assertEqual(1, len(diffs))
        self.assertEqual(RevisionDiff(
            old_ts=datetime.strptime('2020-01-12T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
            new_ts=datetime.strptime('2020-01-15T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
            old_revid=1,
            new_revid=2,
            lines_diffs=[(None, 'old\n'), (None, 'newline\n')]
        ), diffs[0])
