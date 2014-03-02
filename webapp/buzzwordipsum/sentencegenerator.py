import random
import re
import pattern.en as ptn

class SentenceGenerator(object):
    """Generate sentences using a set of templates and a WordPicker"""

    def __init__(self, sentences, wordPicker, seed=None):
        self._wp = wordPicker
        self._sentences = sentences

        if seed is not None:
            random.seed(seed)

    def getSentence(self):
        """Return a random filled sentence"""
        return self.fillTemplate(random.choice(self._sentences))

    def fillTemplate(self, template):
        """Replace all tokens in a template and return it, also capitalising the first letter."""
        s = re.sub(r'\[(.+?)\]', lambda x: self.replaceToken(x.group(1)), template)

        return s[0].upper() + s[1:]

    def replaceToken(self, tokenStr):
        """Replace a token from the sentence template which is a tuple of one or more values.

        The first value indicates the word type and subsequent values will be parsed as shown in this method."""

        # Split the token string on commas and ignore trailing and leading whitespace on each element
        token = tuple(map(str.strip, tokenStr.split(',')))

        # TODO: Not the nicest way of doing the parsing, the sentence template format may need to be changed too.
        if len(token) == 2:
            if token[0] == 'verb':
                if token[1] not in ['PARTICIPLE']:
                    raise ValueError('Invalid tense for verb conjugation')
                # TODO: It hurts to use eval
                return ptn.conjugate(self._wp.pick('verb'), tense=eval('ptn.' + token[1]))
            elif token[0] == 'noun':
                if token[1] not in ['PLURAL']:
                    raise ValueError('Invalid plurality for noun.')
                # Assumes all nouns defined as singulars
                return ptn.pluralize(self._wp.pick('noun'))
        else:
            return self._wp.pick(token[0])

    @classmethod
    def factory(cls, conf, wp):
        """Construct word picker using app config if values are set
        (except WordPicker.wordTypes which must be set)"""

        kwargs = {}
        seed = conf.get('random.seed')
        if seed is not None:
            kwargs['seed'] = seed
        sg = cls(conf['SentenceGenerator.sentences'], wp, **kwargs)
        return sg


class Sentences(object):
    """[...] are used as the template tokens. For 'verb' a second optional argument specifies the tense to be conjugated to"""

    def __init__(self):
        self.TEST = ['We aim to [adverb] [verb] our [adjective] [noun].',
                    '[adverb] [verb, PARTICIPLE] our [noun, PLURAL].']

        self.ALL = ['We aim to [adverb] [verb] our [noun] by [adverb] [verb, PARTICIPLE] the [adjective] [adjective] [noun].',
                    # TODO: May need to use pattern module pluralisation instead of appending s
                    'Our business [verb]s our [noun] to [adverb] and [adverb] [verb] our [adjective] [noun].',
                    '[adverb] [verb, PARTICIPLE] the [adverb] [adjective] [noun] is crucial to our [adjective] [noun].',
                    'In the future, will you be able to [adverb] [verb] [noun, PLURAL] in your business?',
                    'In the [noun] space, industry is [adverb] [verb, PARTICIPLE] its [adjective] [noun, PLURAL].']

