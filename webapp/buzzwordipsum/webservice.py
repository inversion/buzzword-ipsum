# This Python file uses the following encoding: utf-8
from flask import Flask, Response
from webargs import fields, validate
from webargs.flaskparser import use_args
from buzzwordipsum.wordpicker import WordPicker, Words
from buzzwordipsum.sentencegenerator import SentenceGenerator, Sentences

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

    apply_routes(app)
    return app

def make_app_testing():
    app = Flask(__name__)
    app.config.update(DEFAULT_CONFIG)
    app.config.update({
        'ROUTE_NAME': '/buzzwords',
        'DEBUG': True,
        'TESTING': True
    })

    from werkzeug.middleware.shared_data import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), '../../www')
    })

    apply_routes(app)
    return app

def apply_routes(app):
    user_args = {
        "paragraphs": fields.Int(load_default=app.config['DEFAULT_NUM_PARAGRAPHS'], validate=[validate.Range(min=1, max=app.config['MAX_NUM_PARAGRAPHS'])]),
        "type": fields.Str(load_default='sentences', validate=[validate.OneOf(["words", "sentences"])]),
        "format": fields.Str(load_default='text', validate=[validate.OneOf(["html", "text"])]),
        # "template": fields.Str(description='Template should be a string with words to be replaced in square brackets. e.g. "We [verb] our [noun, PLURAL]" will return a string with the bracketed words replaced. To get different forms/tenses, add options after a comma. Supported word types are adverb, noun, adjective, verb. Supported options are verb, PARTICIPLE and noun, PLURAL.')
    }

    @app.route(app.config['ROUTE_NAME'], methods=["GET"])
    @use_args(user_args, location='querystring')
    def buzzwords(args):
        wp = WordPicker.factory(app.config)
        sg = SentenceGenerator.factory(app.config, wp)

        # if 'template' in args:
        #     paragraphs = [sg.fillTemplate(args['template'])]
        # else:
        paragraphs = [makeParagraph(args['type'], wp, sg, app.config) for i in range(args['paragraphs'])]

        if args['format'] == 'text':
            return Response('\n\n'.join(paragraphs) + '\n', content_type='text/plain')
        elif args['format'] == 'html':
            return Response('\n\n'.join('<p>{}</p>'.format(p) for p in paragraphs) + '\n', content_type='text/html')

def makeParagraph(proseType, wp, sg, appconfig):
    if proseType == 'words':
        return ' '.join(wp.pickN('noun', appconfig['WORDS_PER_PARAGRAPH']))
    elif proseType == 'sentences':
        return ' '.join([sg.getSentence() for i in range(appconfig['SENTENCES_PER_PARAGRAPH'])])

if __name__ == "__main__":
    make_app_testing().run()
