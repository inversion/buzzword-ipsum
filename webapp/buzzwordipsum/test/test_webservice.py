from buzzwordipsum import webservice, wordpicker
import unittest
import httplib

class TestWebService(unittest.TestCase):

    def setUp(self):
        webservice.app.config['TESTING'] = True
        webservice.app.config['WordPicker.wordTypes'] = wordpicker.Words().TEST
        webservice.app.config['WordPicker.doShuffles'] = False
        self.app = webservice.app.test_client()

    def testWordPickerFactory(self):
        webservice.app.config = {}
        self.assertRaises(KeyError, webservice.wordPickerFactory)

        testWords = wordpicker.Words().TEST
        webservice.app.config = {'WordPicker.wordTypes': testWords}
        wp = webservice.wordPickerFactory()
        self.assertEquals(wp._wordTypes, testWords)
        self.assertTrue(wp._doShuffles)
        self.assertIsNone(wp._seed)

        webservice.app.config['WordPicker.doShuffles'] = False
        wp = webservice.wordPickerFactory()
        self.assertFalse(wp._doShuffles)

        webservice.app.config['WordPicker.seed'] = 1
        wp = webservice.wordPickerFactory()
        self.assertEquals(wp._seed, 1)

    def testPageFound(self):
        rv = self.app.get(webservice.app.config['ROUTE_NAME'])
        self.assertEquals(rv.status_code, httplib.OK)

    def testNoParamsReturnsDefaultNumberOfNouns(self):
        rv = self.app.get(webservice.app.config['ROUTE_NAME'])
        wp = webservice.wordPickerFactory()
        self.assertEquals(rv.get_data().split(' '), wp.pickN('noun', webservice.app.config['DEFAULT_NUM_WORDS']))
