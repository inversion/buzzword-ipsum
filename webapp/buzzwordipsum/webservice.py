from flask import Flask, Response
from flask.ext import restful
from flask.ext.restful import reqparse
from wordpicker import WordPicker, Words
from sentencegenerator import SentenceGenerator, Sentences

DEFAULT_CONFIG = {
    'DEFAULT_NUM_PARAGRAPHS': 3,
    'MAX_NUM_PARAGRAPHS': 50,
    'SENTENCES_PER_PARAGRAPH': 4,
    'WORDS_PER_PARAGRAPH': 40,
    'WordPicker.wordTypes': Words().ALL,
    'SentenceGenerator.sentences': Sentences().ALL
}

def make_app_production():
    app = Flask(__name__)
    app.config.update(DEFAULT_CONFIG)
    app.config.update({
        'ROUTE_NAME': '/'
    })
    api = restful.Api(app)
    BuzzwordIpsum.appconfig = app.config
    api.add_resource(BuzzwordIpsum, app.config['ROUTE_NAME'])
    return app

def make_app_testing():
    app = Flask(__name__)
    app.config.update(DEFAULT_CONFIG)
    app.config.update({
        'ROUTE_NAME': '/buzzwordsf',
        'DEBUG': True,
        'TESTING': True
    })

    from werkzeug import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), '../../www')
    })

    api = restful.Api(app)
    BuzzwordIpsum.appconfig = app.config
    api.add_resource(BuzzwordIpsum, app.config['ROUTE_NAME'])
    return app

class BuzzwordIpsum(restful.Resource):
    def get(self):
        wp = WordPicker.factory(self.appconfig)
        sg = SentenceGenerator.factory(self.appconfig, wp)

        # TODO: Hack to allow passing of the app config to checkParagraphsArg when run from the RequestParser
        checkParagraphsArg.__defaults__ = (self.appconfig,)

        parser = reqparse.RequestParser()
        parser.add_argument('paragraphs',
                            type=checkParagraphsArg,
                            help='Number of paragraphs should be a positive integer <= ' + str(self.appconfig['MAX_NUM_PARAGRAPHS']),
                            default=self.appconfig['DEFAULT_NUM_PARAGRAPHS'])
        parser.add_argument('type',
                            type=str,
                            choices=('words', 'sentences'),
                            dest='proseType',
                            help='Type should be \'words\' or \'sentences\' (default)',
                            default='sentences')
        parser.add_argument('format',
                            type=str,
                            choices=('html', 'text'),
                            help='Format should be \'html\' or \'text\' (default)',
                            default='text')
        args = parser.parse_args()

        paragraphs = [makeParagraph(args['proseType'], wp, sg, self.appconfig) for i in xrange(args['paragraphs'])]

        if args['format'] == 'text':
            return Response('\n\n'.join(paragraphs) + '\n', content_type='text/plain')
        elif args['format'] == 'html':
            return Response('\n\n'.join('<p>{}</p>'.format(p) for p in paragraphs) + '\n', content_type='text/html')

def makeParagraph(proseType, wp, sg, appconfig):
    if proseType == 'words':
        return ' '.join(wp.pickN('noun', appconfig['WORDS_PER_PARAGRAPH']))
    elif proseType == 'sentences':
        return ' '.join([sg.getSentence() for i in xrange(appconfig['SENTENCES_PER_PARAGRAPH'])])

def checkParagraphsArg(x, appconfig=None):
    try:
        x = int(str(x))
        if x < 1 or x > appconfig['MAX_NUM_PARAGRAPHS']:
            raise ValidationError()
    except ValueError:
        raise ValidationError()
    return x

if __name__ == "__main__":
    make_app_testing().run()
