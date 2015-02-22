from buzzwordipsum.sentencegenerator import SentenceGenerator, Sentences
from buzzwordipsum.wordpicker import WordPicker, Words
import pytest

@pytest.fixture
def sg():
    return SentenceGenerator(Sentences().TEST, WordPicker(Words().TEST, seed=1), seed=1)

def testReplaceToken(sg):
    assert sg.replaceToken('noun') == 'dot-bomb'
    assert sg.replaceToken('verb, PARTICIPLE') == 'virtualising'
    assert sg.replaceToken('verb') == 'virtualise'
    assert sg.replaceToken('noun, PLURAL') == 'milestones'

    with pytest.raises(ValueError):
        sg.replaceToken('verb, PAST')
        sg.replaceToken('noun, SINGULAR')

def testFillTemplate(sg):
    assert sg.fillTemplate(sg._sentences[0]) == 'We aim to virtually virtualise our value-added dot-bomb.'
    assert sg.fillTemplate(sg._sentences[1]) == 'Virtually virtualising our milestones.'

def testFillTemplateWorksOnEmptyString(sg):
    assert sg.fillTemplate('') == ''

def testGetSentence(sg):
    assert sg.getSentence() == 'We aim to virtually virtualise our value-added dot-bomb.'
