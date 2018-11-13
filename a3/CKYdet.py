import os
import sys
from CKY import *
from Grammar import *

class CKYdet:

    @staticmethod
    def read_utterance(fn):
        open_file = open(fn, "r")
        utterances = open_file.readlines()
        result = list()
        for u in utterances:
            utterance = u.strip().split()
            final_utterance = list()
            final_utterance.append('""')
            for word in utterance:
                final_utterance.append('"{}"'.format(word))
            result.append(final_utterance)
        return result

    @staticmethod
    def test(grammar, utterance):
        test_cases = CKYdet.read_utterance(utterance)
        for case in test_cases:
            cky = Grammar.read_grammar(grammar)
            p = cky.b2_bomber(case)
            tmp = p[0][len(p)-1]
            if len(tmp['S']) == 0:
                print "Test case: {} :::::::: No Valid parse".format(" ".join(case[1:]).replace('"', ""))
            else:
                CKYdet.print_parse(p)

    def print_parse(self):
        pass
    