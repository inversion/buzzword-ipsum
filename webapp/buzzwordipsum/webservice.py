from flask import Flask, Response
from flask.ext import restful
from flask.ext.restful import reqparse
import wordpicker

app = Flask(__name__)
app.config.update({
    'ROUTE_NAME': '/buzzwords',
    'DEFAULT_NUM_PARAGRAPHS': 3,
    'MAX_NUM_PARAGRAPHS': 50,
    'SENTENCES_PER_PARAGRAPH': 4,
    'WORDS_PER_PARAGRAPH': 40,
    'WordPicker.wordTypes': wordpicker.Words().ALL
})
api = restful.Api(app)


class BuzzwordIpsum(restful.Resource):
    def get(self):
        wp = wordPickerFactory()
        parser = reqparse.RequestParser()
        parser.add_argument('paragraphs',
                            type=checkParagraphsArg,
                            help='Number of paragraphs: positive integer <= ' + str(app.config['MAX_NUM_PARAGRAPHS']),
                            default=app.config['DEFAULT_NUM_PARAGRAPHS'])
        parser.add_argument('type',
                            type=str,
                            choices=('words'),
                            dest='proseType',
                            help='Type: \'words\'',
                            default='words')
        parser.add_argument('format',
                            type=str,
                            choices=('html', 'text'),
                            help='Format: \'html\' or \'text\' (default)',
                            default='text')
        args = parser.parse_args()

        paragraphs = [makeParagraph(args['proseType'], wp) for i in xrange(args['paragraphs'])]

        if args['format'] == 'text':
            return Response('\n\n'.join(paragraphs) + '\n', content_type='text/plain')
        elif args['format'] == 'html':
            return Response('\n\n'.join('<p>{}</p>'.format(p) for p in paragraphs) + '\n', content_type='text/html')

def makeParagraph(proseType, wp):
    if proseType == 'words':
        return ' '.join(wp.pickN('noun', app.config['WORDS_PER_PARAGRAPH']))

def checkParagraphsArg(x):
    try:
        x = int(str(x))
        if x < 1 or x > app.config['MAX_NUM_PARAGRAPHS']:
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
