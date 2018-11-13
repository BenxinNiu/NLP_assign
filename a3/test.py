from CKYdet import *
from CKY import *


# CKYdet.test("g1.ecfg", "u1a.utt")
# CKYdet.test("g1.ecfg", "u1b.utt")
# CKYdet.test("g2.ecfg", "u2a.utt")
# CKYdet.test("g2.ecfg", "u2b.utt")
# CKYdet.test("g3.ecfg", "u3a.utt")
# CKYdet.test("g3.ecfg", "u3b.utt")
CKYdet.console_runner()
#
# case = ["", '"Bob"', '"admired"', '"the"', '"elephant"']
# # case = ['', '"the"', '"dog"', '"bit"', '"the"', '"rat"']
# grammar = "g1.ecfg"
# cky = Grammar.read_grammar(grammar)
# p = cky.b2_bomber(case)
#
# bomber_head = p[0][len(p) - 1]['S'][0][1]
# a = CKYdet.trace_back_start(p, bomber_head)
# print a