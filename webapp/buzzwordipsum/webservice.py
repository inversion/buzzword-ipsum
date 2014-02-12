from flask import Flask, Response
from flask.ext import restful
from flask.ext.restful import reqparse
import wordpicker

app = Flask(__name__)
app.config.update({
    'ROUTE_NAME': '/buzzwords',
    'DEFAULT_NUM_WORDS': 3,
    'MAX_WORDS_PER_REQUEST': 4096,
    'WordPicker.wordTypes': wordpicker.Words().ALL
})
api = restful.Api(app)


class BuzzwordIpsum(restful.Resource):
    def get(self):
        wp = wordPickerFactory()
        parser = reqparse.RequestParser()
        parser.add_argument('words', type=checkWordsArg, help='Number of words: positive integer <= ' + str(app.config.get('MAX_WORDS_PER_REQUEST', 4096)), default=app.config['DEFAULT_NUM_WORDS'])
        args = parser.parse_args()

        return Response(' '.join(wp.pickN('noun', args.get('words'))), content_type='text/plain')

def checkWordsArg(x):
    try:
        x = int(str(x))
        if x < 1 or x > app.config.get('MAX_WORDS_PER_REQUEST', 4096):
            raise ValidationError()
    except ValueError:
        raise ValidationError()
    return x

def wordPickerFactory():
    """Construct word picker using app config if values are set
    (except WordPicker.wordTypes which must be set)"""

    wpKwargs = {}
    wpSeed = app.config.get('WordPicker.seed')
    if wpSeed is not None:
        wpKwargs['seed'] = wpSeed
    wpDoShuffles = app.config.get('WordPicker.doShuffles')
    if wpDoShuffles is not None:
        wpKwargs['doShuffles'] = wpDoShuffles
    wp = wordpicker.WordPicker(app.config['WordPicker.wordTypes'], **wpKwargs)
    return wp

api.add_resource(BuzzwordIpsum, app.config['ROUTE_NAME'])


if __name__ == "__main__":
    app.run(debug=True)
