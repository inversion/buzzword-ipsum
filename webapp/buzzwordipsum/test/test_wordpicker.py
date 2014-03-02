import unittest
from buzzwordipsum.wordpicker import WordPicker, Words


class TestWordPicker(unittest.TestCase):

    def testInitShuffles(self):
        wp = WordPicker(Words().TEST, seed=1)

        self.assertEquals(wp._wordTypes, {'adjective': ['value-added'], 'verb': ['virtualise'], 'noun': ['dot-bomb', 'milestone', 'cloud'], 'adverb': ['virtually']})

    def testPickWithShuffles(self):
        wp = WordPicker(Words().TEST, seed=1)

        self.assertEquals(wp.pick('noun'), 'dot-bomb')
        self.assertEquals(wp.pick('noun'), 'milestone')
        self.assertEquals(wp.pick('noun'), 'cloud')

        self.assertEquals(wp.pick('noun'), 'cloud')
        self.assertEquals(wp.pick('noun'), 'dot-bomb')
        self.assertEquals(wp.pick('noun'), 'milestone')

        self.assertEquals(wp.pick('noun'), 'cloud')
        self.assertEquals(wp.pick('noun'), 'milestone')
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
            self.assertEquals(wp.pick('noun'), 'milestone')

            self.assertEquals(wp.pick('verb'), 'virtualise')

    def testPickN(self):
        wp = WordPicker(Words().TEST, doShuffles=False)
        self.assertRaises(ValueError, wp.pickN, 'noun', 0)
        self.assertRaises(ValueError, wp.pickN, 'noun', -1)
        self.assertEquals(['cloud'], wp.pickN('noun', 1))
        self.assertEquals(['dot-bomb', 'milestone'], wp.pickN('noun', 2))

