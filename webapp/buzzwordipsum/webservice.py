from flask import Flask, Response
from flask.ext import restful
import wordpicker

app = Flask(__name__)
app.config.update({
    'ROUTE_NAME': '/buzzwords',
    'DEFAULT_NUM_WORDS': 3,
    'WordPicker.wordTypes': wordpicker.Words().ALL
})
api = restful.Api(app)


class BuzzwordIpsum(restful.Resource):
    def get(self):
        wp = wordPickerFactory()

        return Response(' '.join(wp.pickN('noun', app.config['DEFAULT_NUM_WORDS'])), content_type='text/plain')


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
