from buzzwordipsum.wordpicker import WordPicker, Words
import pytest

def testInitShuffles():
    wp = WordPicker(Words().TEST, seed=1)

    assert wp._wordTypes == {'adjective': ['value-added'], 'verb': ['virtualise'], 'noun': ['dot-bomb', 'milestone', 'cloud'], 'adverb': ['virtually']}

def testPickWithShuffles():
    wp = WordPicker(Words().TEST, seed=1)

    assert wp.pick('noun') == 'dot-bomb'
    assert wp.pick('noun') == 'milestone'
    assert wp.pick('noun') == 'cloud'

    assert wp.pick('noun') == 'cloud'
    assert wp.pick('noun') == 'dot-bomb'
    assert wp.pick('noun') == 'milestone'

    assert wp.pick('noun') == 'cloud'
    assert wp.pick('noun') == 'milestone'
    assert wp.pick('noun') == 'dot-bomb'

def testPickWithShufflesOneWordInList():
    wp = WordPicker(Words().TEST, seed=1)

    for i in xrange(2):
        assert wp.pick('adjective') == 'value-added'

def testInitRemovesEmptyButKeepsOthers():
    wp = WordPicker(Words().TEST, doShuffles=False)
    assert 'shouldBeRemoved' not in wp._wordTypes
    assert set(['noun', 'verb', 'adjective', 'adverb']) == set(wp._wordTypes)

def testPickNoShuffles():
    wp = WordPicker(Words().TEST, doShuffles=False)

    # Picking cycles round back to start of list
    for i in xrange(2):
        assert wp.pick('noun') == 'cloud'
        assert wp.pick('noun') == 'dot-bomb'
        assert wp.pick('noun') == 'milestone'

        assert wp.pick('verb') == 'virtualise'

def testPickN():
    wp = WordPicker(Words().TEST, doShuffles=False)
    with pytest.raises(ValueError):
        wp.pickN('noun', 0)
        wp.pickN('noun', -1)
    assert ['cloud'] == wp.pickN('noun', 1)
    assert ['dot-bomb' == 'milestone'], wp.pickN('noun', 2)

