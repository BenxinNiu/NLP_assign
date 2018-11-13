#########################################################
##  CS 4750 (Fall 2018), Assignment #3                 ##
##   Script File Name: Grammar.py                      ##
##       Student Name: Benxin Niu                      ##
##         Login Name: bn2645                          ##
##              MUN #: 201518321                       ##
#########################################################
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
