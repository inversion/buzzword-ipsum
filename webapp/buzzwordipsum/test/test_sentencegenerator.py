from buzzwordipsum.sentencegenerator import SentenceGenerator, Sentences
from buzzwordipsum.wordpicker import WordPicker, Words
import unittest

class TestSentenceGenerator(unittest.TestCase):

    def setUp(self):
        self._sg = SentenceGenerator(Sentences().TEST, WordPicker(Words().TEST, seed=1), seed=1)

    def testReplaceToken(self):
        self.assertEquals(self._sg.replaceToken('noun'), 'dot-bomb')
        self.assertEquals(self._sg.replaceToken('verb, PARTICIPLE'), 'virtualising')
        self.assertEquals(self._sg.replaceToken('verb'), 'virtualise')
        self.assertEquals(self._sg.replaceToken('noun, PLURAL'), 'milestones')

        self.assertRaises(ValueError, self._sg.replaceToken, 'verb, PAST')
        self.assertRaises(ValueError, self._sg.replaceToken, 'noun, SINGULAR')

    def testFillTemplate(self):
        self.assertEquals(self._sg.fillTemplate(self._sg._sentences[0]), 'We aim to virtually virtualise our value-added dot-bomb.')
        self.assertEquals(self._sg.fillTemplate(self._sg._sentences[1]), 'Virtually virtualising our milestones.')

    def testGetSentence(self):
        self.assertEquals(self._sg.getSentence(), 'We aim to virtually virtualise our value-added dot-bomb.')
