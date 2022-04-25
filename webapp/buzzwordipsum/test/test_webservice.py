from buzzwordipsum import webservice as ws, wordpicker
from http import HTTPStatus
import pytest

@pytest.fixture
def wsapp():
    app = ws.make_app_testing()
    app.config['WordPicker.wordTypes'] = wordpicker.Words().TEST
    app.config['WordPicker.doShuffles'] = False
    testClient = app.test_client()
    testClient.config = app.config
    return testClient 

def testPageFound(wsapp):
    rv = wsapp.get(wsapp.config['ROUTE_NAME'])
    assert rv.status_code == HTTPStatus.OK

def testNoParamsReturnsDefaultNumberOfParasWithExpectedWords(wsapp):
    rv = wsapp.get(wsapp.config['ROUTE_NAME'], query_string='type=words')
    wp = wordpicker.WordPicker.factory(wsapp.config)
    assert rv.get_data(as_text=True) == '\n\n'.join([' '.join(wp.pickN('noun', wsapp.config['WORDS_PER_PARAGRAPH'])) for i in range(wsapp.config['DEFAULT_NUM_PARAGRAPHS'])]) + '\n'

def testParagraphsParamReturnsDifferentNumberOfParagraphs(wsapp):
    rv = wsapp.get(wsapp.config['ROUTE_NAME'], query_string='paragraphs=1&type=words')
    wp = wordpicker.WordPicker.factory(wsapp.config)
    assert rv.get_data(as_text=True) == ' '.join(wp.pickN('noun', wsapp.config['WORDS_PER_PARAGRAPH'])) + '\n'

    for q in ['0', 'blah', '', ' ', '1.2', '-1']:
        rv = wsapp.get(wsapp.config['ROUTE_NAME'], query_string='paragraphs=' + q)
        wp = wordpicker.WordPicker.factory(wsapp.config)
        assert rv.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def testMaxNumberOfParagraphsFunctions(wsapp):
    rv = wsapp.get(wsapp.config['ROUTE_NAME'], query_string='paragraphs=' + str(wsapp.config['MAX_NUM_PARAGRAPHS']))
    assert rv.status_code == HTTPStatus.OK

    rv = wsapp.get(wsapp.config['ROUTE_NAME'], query_string='paragraphs=' + str(wsapp.config['MAX_NUM_PARAGRAPHS'] + 1))
    assert rv.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def testHTMLResponse(wsapp):
    rv = wsapp.get(wsapp.config['ROUTE_NAME'], query_string='format=html&paragraphs=1&type=words')
    assert rv.content_type == 'text/html'
    wp = wordpicker.WordPicker.factory(wsapp.config)
    assert rv.get_data(as_text=True) == '<p>' + ' '.join(wp.pickN('noun', wsapp.config['WORDS_PER_PARAGRAPH'])) + '</p>\n'

def testInvalidFormatFails(wsapp):
    rv = wsapp.get(wsapp.config['ROUTE_NAME'], query_string='format=blah')
    assert rv.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def testInvalidTypeFails(wsapp):
    rv = wsapp.get(wsapp.config['ROUTE_NAME'], query_string='type=blah')
    assert rv.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def testValidTypeSucceeds(wsapp):
    rv = wsapp.get(wsapp.config['ROUTE_NAME'], query_string='type=words')
    assert rv.status_code == HTTPStatus.OK
