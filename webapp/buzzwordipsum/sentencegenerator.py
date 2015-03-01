# This Python file uses the following encoding: utf-8
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
        if template == '': return template

        s = re.sub(r'\[(.+?)\]', lambda x: self.replaceToken(x.group(1)), template)

        return s[0].upper() + s[1:]

    def replaceToken(self, tokenStr):
        """Replace a token from the sentence template which is a tuple of one or more values.

        The first value indicates the word type and subsequent values will be parsed as shown in this method."""

        # Split the token string on commas and ignore trailing and leading whitespace on each element
        token = tuple(map(str.strip, tokenStr.split(',')))

        ret = ''

        # TODO: Not the nicest way of doing the parsing, the sentence template format may need to be changed too.
        if len(token) == 2:
            if token[0].lower() == 'verb':
                if token[1] not in ['PARTICIPLE']:
                    raise ValueError('Invalid tense for verb conjugation')
                # TODO: It hurts to use eval
                ret = ptn.conjugate(self._wp.pick('verb'), tense=eval('ptn.' + token[1]))
            elif token[0].lower() == 'noun':
                if token[1] not in ['PLURAL']:
                    raise ValueError('Invalid plurality for noun.')
                # Assumes all nouns defined as singulars
                ret = ptn.pluralize(self._wp.pick('noun'))
        else:
            try:
                ret = self._wp.pick(token[0].lower())
            except KeyError as e:
                ret = '[' + tokenStr + ']'

        # if the token is passed in with Title Case or UPPER CASE, return the words in the same
        if not token[0].islower():
            if token[0].istitle():
                ret = ret.title()
            else:
                ret = ret.upper()

        return ret;

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

        self.ALL = ['We aim to [adverb] [verb] our [noun] by [adverb] [verb, PARTICIPLE] our [adjective] [adjective] [noun, PLURAL].',
                    'Our business [verb]s [noun, PLURAL] to [adverb] and [adverb] [verb] our [adjective] [noun].',
                    '[adverb] [verb, PARTICIPLE] [adverb] [adjective] [noun, PLURAL] is crucial to our [adjective] [noun].',
                    'In the future, will you be able to [adverb] [verb] [noun, PLURAL] in your business?',
                    'In the [noun] space, industry is [adverb] [verb, PARTICIPLE] its [adjective] [noun, PLURAL].',
                    'Going forward, our [adjective] [noun] will deliver value to [noun, PLURAL].',
                    'Change the way you do business - adopt [adjective] [noun, PLURAL].',
                    'Efficiencies will come from [adverb] [verb, PARTICIPLE] our [noun, PLURAL].',
                    'So we can hit the ground running, we will be [adverb] [verb, PARTICIPLE] every [noun] in our space.',
                    'Key players will take ownership of their [noun, PLURAL] by [adverb] [verb, PARTICIPLE] [adjective] [noun, PLURAL].',
                    '[adverb] touching base about [verb, PARTICIPLE] [noun, PLURAL] will make us leaders in the [adjective] [noun] industry.',
                    '[adjective] [noun, PLURAL] [adverb] enable [adjective] [noun, PLURAL] for our [noun, PLURAL].',
                    'Is your [noun] prepared for [adjective] [noun] growth?',
                    '[adjective] [noun, PLURAL] are becoming [adjective] [noun] experts.',
                    'We thrive because of our [adjective] [noun] and [adjective] [noun] culture.',
                    'It\'s critical that we give 110% when [adverb] [verb, PARTICIPLE] [noun, PLURAL].',
                    'Our [noun] development lifecycle enables [adjective], [adjective] [noun, PLURAL].',
                    'We use our [adjective] [noun, PLURAL] to [adverb] manage our [noun] expectations.',
                    'Our [adjective] [noun]™ offers [noun, PLURAL] a suite of [adjective] offerings.']

