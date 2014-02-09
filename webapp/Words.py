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

