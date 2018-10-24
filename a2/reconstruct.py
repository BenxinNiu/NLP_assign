#########################################################
##  CS 4750 (Fall 2018), Assignment #2                 ##
##   Script File Name: reconstruct.py                  ##
##       Student Name: Benxin Niu                      ##
##         Login Name: bn2645                          ##
##              MUN #: 201518321                       ##
#########################################################
from fst import *
import sys
import os
import time


class ConsoleRunner:

    def __init__(self):
        pass

    @staticmethod
    def read_word_list(fn):
        return open(fn).read().strip().split("\n")

    @staticmethod
    def run_with_recording():
        print("Reconstruct.py Started Running:")
        start = int(round(time.time() * 1000))
        if len(sys.argv) == 1:
            print (
                "No files input \n showing usage: python reconstruct.py surface/lexical wlf/wsf file2name file3name... as many file as you want!!")
        else:
            try:
                assert len(sys.argv) >= 4
            except AssertionError:
                raise IOError("Not enough arguments provided {} provided expecting at least{}... exiting".format(len(sys.argv)-1, 3))
            ConsoleRunner.__run()
        end = int(round(time.time() * 1000)) - start
        print ("Exited with no Error. Total runtime {}".format(float(end)))

    @staticmethod
    def __run():
        args = sys.argv
        args.pop(0)
        operation = args.pop(0)
        word_list = ConsoleRunner.read_word_list(args.pop(0))
        if len(args) == 1:
            F = FstGenerator.read_fst(args[0])
            F.print_fst_info()
        else:
            F = ConsoleRunner.__compose_multiple(args)
            F.print_fst_info()
        for w in word_list:
            if operation.lower() == "surface":
                print ("Lexical form: {} \n Reconstructed surface form: "
                       "\n ----------------------------------".format(w))
                F.reconstruct_upper(w)
            elif operation.lower() == "lexical":
                print ("Surface form: {} \n Reconstructed Lexical form: "
                       "\n ----------------------------------".format(w))
                F.reconstruct_lower(w)

    @staticmethod
    def __compose_multiple(args):
        fst_list = list()
        for arg in args:
            f = FstGenerator.read_fst(arg)
            fst_list.append(f)
        if len(fst_list) == 2:
            fst = FstComposer(fst_list[0], fst_list[1])
            return fst.composed_fst
        elif len(fst_list) > 2:
            fst = FstComposer(fst_list[0], fst_list[1])
            idx = 2
            while idx < len(fst_list):
                fst = FstComposer(fst.composed_fst, fst_list[idx])
                idx = idx + 1
            return fst.composed_fst


ConsoleRunner.run_with_recording()

