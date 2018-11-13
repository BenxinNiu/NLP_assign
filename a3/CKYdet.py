#########################################################
##  CS 4750 (Fall 2018), Assignment #3                 ##
##   Script File Name: CKYdet.py                       ##
##       Student Name: Benxin Niu                      ##
##         Login Name: bn2645                          ##
##              MUN #: 201518321                       ##
#########################################################
from Grammar import *


class CKYdet:

    def __init__(self):
        pass

    @staticmethod
    def console_runner():
        args = sys.argv
        args.pop(0)
        if len(args) == 0:
            print("Printing Usage.............")
            print("python CKYdet.py grammar_file utterance_file_name")
        else:
            CKYdet.test(args[0], args[1])

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
                print "utterance:: {}".format(" ".join(case[1:]).replace('"', ""))
                CKYdet.print_parse(p)

    @staticmethod
    def print_parse(p):
        result = []
        bomber_head = p[0][len(p)-1]['S']
        assert len(bomber_head) != 0
        for rule in bomber_head:
            t = CKYdet.trace_back_start(p, rule[1])
            result.append(t)
        for r in result:
            print r

    @staticmethod
    def trace_back_start(p, rule):
        assert len(rule) >= 2
        if len(rule) == 2:
            parse = CKYdet.trace_back_row(p, rule[1], 0, len(p)-1, "")
            return parse
        else:
            parse_row = CKYdet.trace_back_row(p, rule[1], 0, len(p)-1, "")
            parse_col = CKYdet.trace_back_col(p, rule[2], 0, len(p)-1, "")
            return "[S {} {}]".format(parse_row, parse_col)

    @staticmethod
    def trace_back_row(p, target, row_coord, col_coord, result):
        row = p[row_coord]
        for idx in range(col_coord, 0, -1):
            match, target_rule = CKYdet.match(row[idx], target)
            if match and len(target_rule) == 2 and target_rule[1].startswith('"'):
                return result + str(target_rule)
            elif match and len(target_rule) == 2 and not target_rule[1].startswith('"'):
                rule = row[idx][target_rule[1]]
                return result + "[{} {}]".format(target_rule[0], str(rule[0][1]))
            elif match and len(target_rule) >=2:
                parse_row = CKYdet.trace_back_row(p, target_rule[1], row_coord, idx, result)
                parse_col = CKYdet.trace_back_col(p, target_rule[2], row_coord, idx, result)
                return "[{} {} {}]".format(target_rule[0], parse_row, parse_col)
        return result

    @staticmethod
    def trace_back_col(p, target, row_coord, col_coord, result):
        for idx in range(row_coord, len(p)-1):
            match, target_rule = CKYdet.match(p[idx][col_coord], target)
            if match and len(target_rule) == 2 and target_rule[1].startswith('"'):
                return result + str(target_rule)
            elif match and len(target_rule) == 2 and not target_rule[1].startswith('"'):
                rule = p[idx][col_coord][target_rule[1]]
                return result + "[{} {}]".format(target_rule[0], str(rule[0][1]))
            elif match and len(target_rule) >=2:
                parse_row = CKYdet.trace_back_row(p, target_rule[1], idx, col_coord, result)
                parse_col = CKYdet.trace_back_col(p, target_rule[2], idx, col_coord, result)
                return "[{} {} {}]".format(target_rule[0], parse_row, parse_col)
        return result

    @staticmethod
    def match(entry, target):
        rules = entry[target]
        matched = len(rules) != 0
        if matched:
            # TODO update this to enable printing multiple parses
            return matched, rules[0][1]
        else:
            return False, []


CKYdet.console_runner()