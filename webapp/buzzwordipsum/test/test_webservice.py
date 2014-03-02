from buzzwordipsum import webservice as ws, wordpicker
import unittest
import httplib

class TestWebService(unittest.TestCase):

    def setUp(self):
        ws.app.config['TESTING'] = True
        ws.app.config['WordPicker.wordTypes'] = wordpicker.Words().TEST
        ws.app.config['WordPicker.doShuffles'] = False
        self.app = ws.app.test_client()

    def testPageFound(self):
        rv = self.app.get(ws.app.config['ROUTE_NAME'])
        self.assertEquals(rv.status_code, httplib.OK)

    def testNoParamsReturnsDefaultNumberOfParasWithExpectedWords(self):
        rv = self.app.get(ws.app.config['ROUTE_NAME'])
        wp = wordpicker.WordPicker.factory(ws.app.config)
        self.assertEquals(rv.get_data(),
                            '\n\n'.join([' '.join(wp.pickN('noun', ws.app.config['WORDS_PER_PARAGRAPH'])) for i in xrange(ws.app.config['DEFAULT_NUM_PARAGRAPHS'])]) + '\n')

    def testParagraphsParamReturnsDifferentNumberOfParagraphs(self):
        rv = self.app.get(ws.app.config['ROUTE_NAME'], query_string='paragraphs=1')
        wp = wordpicker.WordPicker.factory(ws.app.config)
        self.assertEquals(rv.get_data(), ' '.join(wp.pickN('noun', ws.app.config['WORDS_PER_PARAGRAPH'])) + '\n')

        for q in ['0', 'blah', '', ' ', '1.2', '-1']:
            rv = self.app.get(ws.app.config['ROUTE_NAME'], query_string='paragraphs=' + q)
            wp = wordpicker.WordPicker.factory(ws.app.config)
            self.assertEquals(rv.status_code, httplib.BAD_REQUEST)

    def testMaxNumberOfParagraphsFunctions(self):
        rv = self.app.get(ws.app.config['ROUTE_NAME'], query_string='paragraphs=' + str(ws.app.config['MAX_NUM_PARAGRAPHS']))
        self.assertEquals(rv.status_code, httplib.OK)

        rv = self.app.get(ws.app.config['ROUTE_NAME'], query_string='paragraphs=' + str(ws.app.config['MAX_NUM_PARAGRAPHS'] + 1))
        self.assertEquals(rv.status_code, httplib.BAD_REQUEST)
        self.assertEquals(rv.data, '{"message": "Number of paragraphs: positive integer <= ' + str(ws.app.config['MAX_NUM_PARAGRAPHS']) + '"}')

    def testHTMLResponse(self):
        rv = self.app.get(ws.app.config['ROUTE_NAME'], query_string='format=html&paragraphs=1')
        self.assertEquals(rv.content_type, 'text/html')
        wp = wordpicker.WordPicker.factory(ws.app.config)
        self.assertEquals(rv.data, '<p>' + ' '.join(wp.pickN('noun', ws.app.config['WORDS_PER_PARAGRAPH'])) + '</p>\n')

    def testInvalidFormatFails(self):
        rv = self.app.get(ws.app.config['ROUTE_NAME'], query_string='format=blah')
        self.assertEquals(rv.status_code, httplib.BAD_REQUEST)

    def testInvalidTypeFails(self):
        rv = self.app.get(ws.app.config['ROUTE_NAME'], query_string='type=blah')
        self.assertEquals(rv.status_code, httplib.BAD_REQUEST)

    def testValidTypeSucceeds(self):
        rv = self.app.get(ws.app.config['ROUTE_NAME'], query_string='type=words')
        self.assertEquals(rv.status_code, httplib.OK)
