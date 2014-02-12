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
        # TODO: Not ideal that we need to remember to put this back at the end
        # of the test
        oldWebServiceConf = webservice.app.config
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

        webservice.app.config = oldWebServiceConf

    def testPageFound(self):
        rv = self.app.get(webservice.app.config['ROUTE_NAME'])
        self.assertEquals(rv.status_code, httplib.OK)

    def testNoParamsReturnsDefaultNumberOfNouns(self):
        rv = self.app.get(webservice.app.config['ROUTE_NAME'])
        wp = webservice.wordPickerFactory()
        self.assertEquals(rv.get_data().split(' '), wp.pickN('noun', webservice.app.config['DEFAULT_NUM_WORDS']))

    def testWordsParamReturnsDifferentNumberOfWords(self):
        rv = self.app.get(webservice.app.config['ROUTE_NAME'], query_string='words=1')
        wp = webservice.wordPickerFactory()
        self.assertEquals(rv.get_data(), wp.pick('noun'))

        for q in ['0', 'blah', '', ' ', '1.2', '-1']:
            rv = self.app.get(webservice.app.config['ROUTE_NAME'], query_string='words=' + q)
            wp = webservice.wordPickerFactory()
            self.assertEquals(rv.status_code, httplib.BAD_REQUEST)

    def testMaxNumberOfWordsFunctions(self):
        rv = self.app.get(webservice.app.config['ROUTE_NAME'], query_string='words=' + str(webservice.app.config['MAX_WORDS_PER_REQUEST']))
        self.assertEquals(rv.status_code, httplib.OK)

        rv = self.app.get(webservice.app.config['ROUTE_NAME'], query_string='words=' + str(webservice.app.config['MAX_WORDS_PER_REQUEST'] + 1))
        self.assertEquals(rv.status_code, httplib.BAD_REQUEST)
        self.assertEquals(rv.data, '{"message": "Number of words: positive integer <= ' + str(webservice.app.config['MAX_WORDS_PER_REQUEST']) + '"}')

