from flask import Flask, Response
from flask.ext import restful
from flask.ext.restful import reqparse
from wordpicker import WordPicker, Words
from sentencegenerator import SentenceGenerator, Sentences

app = Flask(__name__)
app.config.update({
    'ROUTE_NAME': '/',
    'DEFAULT_NUM_PARAGRAPHS': 3,
    'MAX_NUM_PARAGRAPHS': 50,
    'SENTENCES_PER_PARAGRAPH': 4,
    'WORDS_PER_PARAGRAPH': 40,
    'WordPicker.wordTypes': Words().ALL,
    'SentenceGenerator.sentences': Sentences().ALL
})
api = restful.Api(app)


class BuzzwordIpsum(restful.Resource):
    def get(self):
        wp = WordPicker.factory(app.config)
        sg = SentenceGenerator.factory(app.config, wp)

        parser = reqparse.RequestParser()
        parser.add_argument('paragraphs',
                            type=checkParagraphsArg,
                            help='Number of paragraphs: positive integer <= ' + str(app.config['MAX_NUM_PARAGRAPHS']),
                            default=app.config['DEFAULT_NUM_PARAGRAPHS'])
        parser.add_argument('type',
                            type=str,
                            choices=('words', 'sentences'),
                            dest='proseType',
                            help='Type: \'words\', \'sentences\'',
                            default='words')
        parser.add_argument('format',
                            type=str,
                            choices=('html', 'text'),
                            help='Format: \'html\' or \'text\' (default)',
                            default='text')
        args = parser.parse_args()

        paragraphs = [makeParagraph(args['proseType'], wp, sg) for i in xrange(args['paragraphs'])]

        if args['format'] == 'text':
            return Response('\n\n'.join(paragraphs) + '\n', content_type='text/plain')
        elif args['format'] == 'html':
            return Response('\n\n'.join('<p>{}</p>'.format(p) for p in paragraphs) + '\n', content_type='text/html')

def makeParagraph(proseType, wp, sg):
    if proseType == 'words':
        return ' '.join(wp.pickN('noun', app.config['WORDS_PER_PARAGRAPH']))
    elif proseType == 'sentences':
        return ' '.join([sg.getSentence() for i in xrange(app.config['SENTENCES_PER_PARAGRAPH'])])

def checkParagraphsArg(x):
    try:
        x = int(str(x))
        if x < 1 or x > app.config['MAX_NUM_PARAGRAPHS']:
            raise ValidationError()
    except ValueError:
        raise ValidationError()
    return x

api.add_resource(BuzzwordIpsum, app.config['ROUTE_NAME'])


if __name__ == "__main__":
    app.run(debug=True)
