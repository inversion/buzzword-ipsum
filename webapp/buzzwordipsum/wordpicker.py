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
        for wordType in self._wordTypes.keys():
            words = self._wordTypes[wordType]
            if len(words) == 0:
                del self._wordTypes[wordType]
                logging.warn('Word type \'' + wordType + '\' has no words, ignoring it.')

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
        return [self.pick(wordType) for i in xrange(n)]


class Words(object):

    def __init__(self):
        #NB: verbs must make sense as -ing and -e, i.e. "calibrating/calibrate" is fine but not "growing/growe"
        #could fix with a second array (painful) or making an array of pairs, i.e. {[growing, grow], virtualising, virtualise])
        self.ALL = {'verb': ['virtualising', 'synergising',
                                        'calibrating',
                                        #'growing', 'impacting',
                                            'leveraging',
                                        #'transforming',
                                            'revolutionizing',
                                        #'relaying',
                                            'deep diving',
                                        'offshoring'],
            'noun': ['cloud', 'dot-bomb', 'user experience', 'milestones',
                        'organic growth', 'alignment', 'ballpark figure',
                        'synergy', 'big data', 'bandwidth', 'brand',
                        'corecompetency', 'enterprise', 'low hanging fruit',
                        'visibility', 'diversity', 'capability', 'platform',
                        'core assets', 'best practice', 'proposition',
                        'enterprise', 'stack'],
            'adjective': ['value-added', 'mission critical', 'immersive',
                                'customer-focused', 'holistic', 'mobile',
                                'end-to-end', 'long-term'],
            'adverb': ['virtually', 'strategically', 'reliably', 'globally',
                            'proactively', 'iteratively', 'ethically',
                            'intelligently']
            }

        self.TEST = {'verb': ['virtualising'],
                'noun': ['cloud', 'dot-bomb', 'milestones'],
                'adjective': ['value-added'],
                'adverb': ['virtually'],
                'shouldBeRemoved': []}

