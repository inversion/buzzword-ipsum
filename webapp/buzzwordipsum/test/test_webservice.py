from buzzwordipsum import webservice as ws, wordpicker
import httplib
import pytest

@pytest.fixture
def wsapp():
    ws.app.config['TESTING'] = True
    ws.app.config['WordPicker.wordTypes'] = wordpicker.Words().TEST
    ws.app.config['WordPicker.doShuffles'] = False
    return ws.app.test_client()

def testPageFound(wsapp):
    rv = wsapp.get(ws.app.config['ROUTE_NAME'])
    assert rv.status_code == httplib.OK

def testNoParamsReturnsDefaultNumberOfParasWithExpectedWords(wsapp):
    rv = wsapp.get(ws.app.config['ROUTE_NAME'])
    wp = wordpicker.WordPicker.factory(ws.app.config)
    assert rv.get_data() == '\n\n'.join([' '.join(wp.pickN('noun', ws.app.config['WORDS_PER_PARAGRAPH'])) for i in xrange(ws.app.config['DEFAULT_NUM_PARAGRAPHS'])]) + '\n'

def testParagraphsParamReturnsDifferentNumberOfParagraphs(wsapp):
    rv = wsapp.get(ws.app.config['ROUTE_NAME'], query_string='paragraphs=1')
    wp = wordpicker.WordPicker.factory(ws.app.config)
    assert rv.get_data() == ' '.join(wp.pickN('noun', ws.app.config['WORDS_PER_PARAGRAPH'])) + '\n'

    for q in ['0', 'blah', '', ' ', '1.2', '-1']:
        rv = wsapp.get(ws.app.config['ROUTE_NAME'], query_string='paragraphs=' + q)
        wp = wordpicker.WordPicker.factory(ws.app.config)
        assert rv.status_code == httplib.BAD_REQUEST

def testMaxNumberOfParagraphsFunctions(wsapp):
    rv = wsapp.get(ws.app.config['ROUTE_NAME'], query_string='paragraphs=' + str(ws.app.config['MAX_NUM_PARAGRAPHS']))
    assert rv.status_code == httplib.OK

    rv = wsapp.get(ws.app.config['ROUTE_NAME'], query_string='paragraphs=' + str(ws.app.config['MAX_NUM_PARAGRAPHS'] + 1))
    assert rv.status_code == httplib.BAD_REQUEST
    assert rv.data == '{"message": "Number of paragraphs: positive integer <= ' + str(ws.app.config['MAX_NUM_PARAGRAPHS']) + '"}'

def testHTMLResponse(wsapp):
    rv = wsapp.get(ws.app.config['ROUTE_NAME'], query_string='format=html&paragraphs=1')
    assert rv.content_type == 'text/html'
    wp = wordpicker.WordPicker.factory(ws.app.config)
    assert rv.data == '<p>' + ' '.join(wp.pickN('noun', ws.app.config['WORDS_PER_PARAGRAPH'])) + '</p>\n'

def testInvalidFormatFails(wsapp):
    rv = wsapp.get(ws.app.config['ROUTE_NAME'], query_string='format=blah')
    assert rv.status_code == httplib.BAD_REQUEST

def testInvalidTypeFails(wsapp):
    rv = wsapp.get(ws.app.config['ROUTE_NAME'], query_string='type=blah')
    assert rv.status_code == httplib.BAD_REQUEST

def testValidTypeSucceeds(wsapp):
    rv = wsapp.get(ws.app.config['ROUTE_NAME'], query_string='type=words')
    assert rv.status_code == httplib.OK
