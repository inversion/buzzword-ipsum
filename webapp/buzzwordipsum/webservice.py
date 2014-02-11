from flask import Flask
from buzzwordipsum import wordpicker
app = Flask(__name__)

app.config.update({
    'ROUTE_NAME': '/buzzwords',
    'DEFAULT_NUM_WORDS': 3,
    'WordPicker.wordTypes': wordpicker.Words().ALL
})


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


@app.route(app.config['ROUTE_NAME'])
def main():
    wp = wordPickerFactory()

    return ' '.join(wp.pickN('noun', app.config['DEFAULT_NUM_WORDS']))


if __name__ == "__main__":
    app.run()
