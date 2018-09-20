#########################################################
##  CS 4750 (Fall 2018), Assignment #1, Question #2    ##
##   Script File Name: tcomp2.py                       ##
##       Student Name: Benxin Niu                      ##
##         Login Name: bn2645                          ##
##              MUN #: 201518321                       ##
#########################################################
import sys
import os
import time


class ConsoleRunner:

    def __init__(self):
        pass

    @staticmethod
    def run_with_recording():
        print("tcomp2.py A1 Q2 Started Running:")
        start = int(round(time.time() * 1000))
        if len(sys.argv) == 1:
            print (
                "No files input \n showing usage: python tcomp2.py filename file2name file3name... as many file as you want!!")
        else:
            ConsoleRunner.__run()
        end = int(round(time.time() * 1000)) - start
        print ("Exited with no Error. Total runtime {}".format(float(end)))

    @staticmethod
    def __run():
        args = sys.argv
        args.pop(0)
        master_file = args.pop(0)
        master_list = FileProcessor.file_to_list(master_file)
        sim_list = list()
        for f in args:
            wl = FileProcessor.file_to_list(f)
            sim = Comparator.sim(master_list, wl)
            sim_list.append(sim)
            print("Sim(\"{f1}\", \"{f2}\") = {r}".format(f1=master_file, f2=f, r=sim))
        try:
            max_sim = max(sim_list)
            f = args[sim_list.index(max_sim)]
            print("File {} is most similar with master file {} ".format(f, master_file))
        except ValueError:
            raise Exception("Error in finding the most similar file")


class FileProcessor:

    def __init__(self):
        pass

    @staticmethod
    def file_to_list(path):
        if os.path.isfile(path):
            data_list = list()
            try:
                open_file = open(path, "r")
                lines = open_file.readlines()
                for line in lines:
                    sub_list = line.strip().split()
                    data_list.extend(sub_list)
                return data_list
            except IOError:
                raise IOError("Failure in opening {}".format(path))
        else:
            raise AssertionError('file does not exist or is not a file! {} \n'.format(path))


class Comparator:

    def __init__(self):
        pass

    @staticmethod
    def sim(wl1, wl2):
        sd = Comparator.__sd(wl1, wl2)
        nw = Comparator.__nw(wl1) + Comparator.__nw(wl2)
        sim = 1.0 - (float(sd) / nw)
        return round(sim, 3)

    @staticmethod
    def __nw(word_list):
        return len(set(word_list))

    @staticmethod
    def __sd(word_list1, word_list2):
        wl1 = list(set(word_list1))
        wl2 = list(set(word_list2))
        result = Comparator.__dc(wl1, wl2) + Comparator.__dc(wl2, wl1)
        return result

    @staticmethod
    def __dc(wl1, wl2):
        dc_sum = 0
        for word in wl1:
            try:
                idx = wl2.index(word)
            except ValueError:
                dc_sum = dc_sum + 1
        return dc_sum


ConsoleRunner.run_with_recording()

