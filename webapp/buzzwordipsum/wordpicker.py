# This Python file uses the following encoding: utf-8
import random
import logging


class WordPicker(object):

    def __init__(self, wordTypes, doShuffles=True, seed=None):
        self._wordTypes = wordTypes
        self._doShuffles = doShuffles
        self._seed = seed
        if seed is not None:
            random.seed(seed)

        # Remove empty word types
        for wordType in list(self._wordTypes.keys()):
            words = self._wordTypes[wordType]
            if len(words) == 0:
                del self._wordTypes[wordType]
                logging.warning('Word type \'' + wordType + '\' has no words, ignoring it.')

        # Shuffle each list initially
        if self._doShuffles:
            self._wordTypes.update((wordType, sorted(words, key=lambda k: random.random())) for wordType, words in sorted(self._wordTypes.items()))

        # Set up counters to record when each list is exhausted so it can be
        # reshuffled
        self._wordTypePositions = {wordType: 0 for wordType in self._wordTypes.keys()}

    def pick(self, wordType):
        """Pick a word from the specified type at the point and advance the pointer for that list.
           When the end of the list is reached it will be shuffled (if self._doShuffles is True) and the pointer will be reset to 0."""

        if self._wordTypePositions[wordType] == len(self._wordTypes[wordType]):
            self._wordTypePositions[wordType] = 0
            if self._doShuffles:
                self._wordTypes[wordType] = sorted(self._wordTypes[wordType], key=lambda k: random.random())

        word = self._wordTypes[wordType][self._wordTypePositions[wordType]]
        self._wordTypePositions[wordType] += 1
        return word

    def pickN(self, wordType, n):
        if n < 1:
            raise ValueError('Must pick >= 1 words')
        return [self.pick(wordType) for i in range(n)]

    @classmethod
    def factory(cls, conf):
        """Construct word picker using app config if values are set
        (except WordPicker.wordTypes which must be set)"""

        kwargs = {}
        seed = conf.get('random.seed')
        if seed is not None:
            kwargs['seed'] = seed
        doShuffles = conf.get('WordPicker.doShuffles')
        if doShuffles is not None:
            kwargs['doShuffles'] = doShuffles
        wp = cls(conf['WordPicker.wordTypes'], **kwargs)
        return wp


class Words(object):

    def __init__(self):
        self.ALL = {'verb': ['virtualise', 'synergise', 'calibrate',
                             'grow', 'impact', 'leverage',
                             'transform', 'revolutionize', 'relay',
                             'deep-dive', 'offshore', 'integrate',
                             'reuse', 'align', 'connect',
                             'monetize', 'strategize', 'incentivize',
                             'invest', 'engineer', 'facilitate', 'right-size', 'innovate', 'productize'],
            'noun': ['dot-bomb', 'user experience', 'milestone',
                         'alignment', 'ballpark figure',
                         'bandwidth', 'brand',
                        'core competency', 'enterprise',
                        'visibility', 'diversity', 'capability', 'platform',
                        'core asset', 'best practice', 'proposition',
                        'enterprise', 'stack', 'capability', 'market focus',
                        'executive search', 'prince2 practitioner', 'stand-up',
                        'paradigm shift', 'silo', 'deliverable',
                        'innovation', 'team player', 'architecture',
                        'stakeholder', 'standpoint', 'game changer',
                        'agile workflow', 'emerging market', 'cloud',
                        'synergy', 'low hanging fruit', 'big data',
                        'organic growth', 'step-change', 'driver',
                        'action point', 'vertical', 'standard setter',
                        'industry leader', 'knowledge transfer', 'intrapreneur', 'imagineering', 'product', 'creator', 'digital nomad', 'growth hacker',
                        'blockchain', 'crypto', 'smart contract','NFT'],
            'adjective': ['value-added', 'mission critical', 'immersive',
                                'customer-focused', 'holistic', 'mobile',
                                'end-to-end', 'long-term', 'proactive',
                                'best-of-breed', 'seamless', 'competitive',
                                'actionable', 'innovative', 'best-in-class',
                                'company-wide', 'senior', 'cloud native',
                                'corporate', 'wholesale', 'next-generation',
                                'world-class', 'unparalleled', 'self-driving'],
            'adverb': ['effectively', 'dynamically', 'virtually', 'strategically', 'reliably', 'globally',
                            'proactively', 'iteratively', 'ethically', 'intelligently', 'conservatively']
            }

        self.TEST = {'verb': ['virtualise'],
                'noun': ['cloud', 'dot-bomb', 'milestone'],
                'adjective': ['value-added'],
                'adverb': ['virtually'],
                'shouldBeRemoved': []}


