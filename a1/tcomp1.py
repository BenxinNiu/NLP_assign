#########################################################
##  CS 4750 (Fall 2018), Assignment #1, Question #1    ##
##   Script File Name: tcomp1.py                       ##
##       Student Name: Benxin Niu                      ##
##         Login Name: bn2645                          ##
##              MUN #: 201518321                       ##
#########################################################
import os
import sys
import collections
import time


class ConsoleRunner:

    def __init__(self):
        pass

    @staticmethod
    def run_with_recording():
        print("tcomp1.py A1 Q1 Started Running:")
        start = int(round(time.time() * 1000))
        ConsoleRunner.__run()
        end = int(round(time.time() * 1000)) - start
        print ("Exited with no Error. Total runtime {}".format(float(end)))

    @staticmethod
    def __run():
        args = sys.argv
        args.pop(0)
        n = int(args.pop(1))
        master = args.pop(0)
        master_file_processed = FileProcessor.file_to_list(master)
        master_ngs = FileProcessor.ngram(master_file_processed, n)
        master_vector = NgramFreqVector(master_ngs).get_freq_vector()
        sim_list = list()
        for arg in args:
            file_processed = FileProcessor.file_to_list(arg)
            ngs = FileProcessor.ngram(file_processed, n)
            vector = NgramFreqVector(ngs).get_freq_vector()
            score = VectorComparator.sim(master_vector, vector)
            sim_list.append(score)
            print("Sim( \"{f1}\", \"{f2}\" ) = {r}".format(f1=master, f2=arg, r=score))
        try:
            max_sim = max(sim_list)
            f = args[sim_list.index(max_sim)]
            print ("File {} is most similar with master file {} ".format(f, master))
        except KeyError:
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

    @staticmethod
    def ngram(data_list, n):
        if isinstance(n, int):
            ngram_list = []
            for word in data_list:
                subngrams = FileProcessor.subngram(word, n)
                ngram_list.extend(subngrams)
            return ngram_list
        else:
            raise AssertionError("n is not an Integer!!!!!! check method of ngram()")

    @staticmethod
    def subngram(chars, num):
        ngrams = []
        if len(chars) == num:
            ngrams.append(chars)
            return ngrams
        elif len(chars) > num:
            for i in range(len(chars)-num+1):
                ngrams.append(chars[i:i+num])
            return ngrams
        else:
            return []


class VectorComparator:

    def __init__(self):
        pass

    @staticmethod
    def __diff(v1, v2):
        sum = 0
        for key, val in v1.items():
            try:
                freq_occurrence = v2.pop(key)
                sum = float(sum) + abs(val - freq_occurrence)
            except KeyError:
                sum = sum + val
        for key, val in v2.items():
            sum = sum + val
        return sum

    @staticmethod
    def sim(v1, v2):
        diff = VectorComparator.__diff(v1, v2)
        sim = 1 - (float(diff) / 2)
        return round(sim, 3)


class NgramFreqVector:

    def __init__(self, ngrams):
        self.ngrams = ngrams
        self.__ngram_dc = self.__dc(ngrams)
        self.__ngram_count = self.__count(ngrams)
        self.__vector = self.__vector(ngrams)

    def __dc(self, ngrams):
        return len(set(ngrams))

    def __count(self, ngrams):
        return len(ngrams)

    def __vector(self, ngrams):
        dedup_ngrams = set(ngrams)
        freq_vector = collections.OrderedDict()
        for item in dedup_ngrams:
            occurrence = ngrams.count(item)
            freq_vector[item] = float(occurrence) / self.__ngram_count

        return freq_vector

    def get_freq_vector(self):
        return self.__vector

    def get_dc_ngrams(self):
        return self.__ngram_dc

    def get_count_ngrams(self):
        return self.__ngram_count


ConsoleRunner.run_with_recording()
