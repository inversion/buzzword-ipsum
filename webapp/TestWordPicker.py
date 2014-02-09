import unittest
from WordPicker import WordPicker
from Words import Words


class TestWordPicker(unittest.TestCase):

    def testInitShuffles(self):
        wp = WordPicker(Words().TEST, seed=1)

        self.assertEquals(wp._wordTypes, {'adjective': ['value-added'], 'verb': ['virtualising'], 'noun': ['dot-bomb', 'milestones', 'cloud'], 'adverb': ['virtually']})

    def testPickWithShuffles(self):
        wp = WordPicker(Words().TEST, seed=1)

        self.assertEquals(wp.pick('noun'), 'dot-bomb')
        self.assertEquals(wp.pick('noun'), 'milestones')
        self.assertEquals(wp.pick('noun'), 'cloud')

        self.assertEquals(wp.pick('noun'), 'cloud')
        self.assertEquals(wp.pick('noun'), 'dot-bomb')
        self.assertEquals(wp.pick('noun'), 'milestones')

        self.assertEquals(wp.pick('noun'), 'cloud')
        self.assertEquals(wp.pick('noun'), 'milestones')
        self.assertEquals(wp.pick('noun'), 'dot-bomb')

    def testPickWithShufflesOneWordInList(self):
        wp = WordPicker(Words().TEST, seed=1)

        for i in xrange(2):
            self.assertEquals(wp.pick('adjective'), 'value-added')

    def testInitRemovesEmptyButKeepsOthers(self):
        wp = WordPicker(Words().TEST, doShuffles=False)
        self.assertNotIn('shouldBeRemoved', wp._wordTypes)
        self.assertEquals(set(['noun', 'verb', 'adjective', 'adverb']), set(wp._wordTypes))

    def testPickNoShuffles(self):
        wp = WordPicker(Words().TEST, doShuffles=False)

        # Picking cycles round back to start of list
        for i in xrange(2):
            self.assertEquals(wp.pick('noun'), 'cloud')
            self.assertEquals(wp.pick('noun'), 'dot-bomb')
            self.assertEquals(wp.pick('noun'), 'milestones')

            self.assertEquals(wp.pick('verb'), 'virtualising')
