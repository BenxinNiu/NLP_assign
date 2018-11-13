import sys
import os
from CKY import *


class Grammar:


    @staticmethod
    def read_grammar(fn):
        open_file = open(fn, "r")
        grammar = open_file.readlines()
        rules, non_terminals =list(), list()
        for r in grammar:
            rule = r.strip().replace("->", "").split()
            rules.append(rule)
            non_terminals.append(rule[0])
        non_terminals = set(non_terminals)
        return CKY(rules, non_terminals)

        # production_rules = list()
        # for rule in rules:
        #     assert len(rule) >= 2
        #     if len(rule) == 2 and rule[1] in terminals:
        #         n = [rule[0]]
        #         for r in rules:
        #             if r[0] == rule[1]:
        #                 replace = n + r[1:]
        #                 production_rules.append(replace)
        #     else:
        #         production_rules.append(rule)
        # for r in production_rules:
        #    print r
