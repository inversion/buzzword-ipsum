import random
import logging


class WordPicker(object):

    def __init__(self, wordTypes, doShuffles=True, seed=None):
        self._wordTypes = wordTypes
        self._doShuffles = doShuffles
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
