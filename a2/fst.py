#########################################################
##  CS 4750 (Fall 2018), Assignment #2                 ##
##   Script File Name: fst.py                          ##
##       Student Name: Benxin Niu                      ##
##         Login Name: bn2645                          ##
##              MUN #: 201518321                       ##
#########################################################
import os
import sys
import collections


class FstComposer:

    def __init__(self, F1, F2):
        self.num_state_validator = F1.num_state * F2.num_state
        self.chars_validator = F1.chars.extend(F2.chars)
        self.state_indicator = 2
        self.composed_fst = FST(self.num_state_validator, str(self.chars_validator))
        self.__compose(F1, F2)
        # self.composed_fst.print_fst_info()

    def __compose(self, F1, F2):
        new_states = self.__compose_states(F1, F2)
        for q1_q2 in new_states:
            for q3_q4 in new_states:
                self.__add_transitions(F1, F2, q1_q2, q3_q4, new_states)

    def __add_transitions(self, F1, F2, q1_q2, q3_q4, new_states):
        q1, q2 = q1_q2["state"][0], q1_q2["state"][1]
        q3, q4 = q3_q4["state"][0], q3_q4["state"][1]
        for trans1 in F1.transitions:
            for trans2 in F2.transitions:
                if trans1.source == q1 and trans1.dest == q3 and trans2.source == q2 and trans2.dest == q4:
                    if trans1.upper == trans2.lower:
                        new_transition = Transition(q1_q2["new_s_name"], trans1.lower, trans2.upper, q3_q4["new_s_name"])
                        self.composed_fst.add_transitions(new_transition)
                    if trans1.upper == "-" and trans2.lower != "-":
                        dest = self.__find_new_name(new_states, [str(q3), str(q2)])
                        new_transition = Transition(q1_q2["new_s_name"], trans1.lower, "-", dest)
                        self.composed_fst.add_transitions(new_transition)
                    if trans1.upper != "-" and trans2.lower == "-":
                        dest = self.__find_new_name(new_states, [str(q1), str(q4)])
                        new_transition = Transition(q1_q2["new_s_name"], "-", trans2.upper, dest)
                        self.composed_fst.add_transitions(new_transition)

    def __compose_states(self, F1, F2):
        states = list()
        index = 1
        for s1, f1 in F1.states.items():
            for s2, f2 in F2.states.items():
                new_s = list()
                s_info = dict()
                new_s.append(s1)
                new_s.append(s2)
                s_info["state"] = new_s
                s_info["final"] = f1 and f2
                s_info["new_s_name"] = str(index)
                index = index + 1
                self.composed_fst.add_state(s_info["new_s_name"], s_info["final"])
                states.append(s_info)
        return states

    def __find_new_name(self, states_list, state):
        for s in states_list:
            if s["state"] == state:
                return s["new_s_name"]


class FstGenerator:

    def __init__(self):
        pass

    @staticmethod
    def read_fst(fn):
        if os.path.isfile(fn):
            try:
                open_file = open(fn, "r")
                lines = open_file.readlines()
                num, chars = lines.pop(0).split()
                fst_instance = FST(num, chars)
                for line in lines:
                    if not line.startswith('  '):
                        s, f = line.strip().split()
                        fst_instance.add_state(s, f)
                    elif line.startswith('  '):
                        l, u, d = line.strip().split()
                        transition = Transition(s, l, u, d)
                        fst_instance.add_transitions(transition)
                # fst_instance.print_fst_info()
                return fst_instance
            except IOError:
                raise IOError("Failure in opening {}".format(fn))
        else:
            raise AssertionError('file does not exist or is not a file! {} \n'.format(fn))


class FST:

    def __init__(self, num, chars):
        self.num_state = int(num)
        self.chars = chars.split()
        self.states = collections.OrderedDict()
        self.transitions = list()

    def add_state(self, state, f):
        is_final = f == "F"
        self.states[state] = is_final

    def add_transitions(self, transition):
        self.transitions.append(transition)

    def list_states(self):
        print("FST has {} states".format(self.num_state))
        for s, f in self.states.items():
            print ("state: {}, is final: {}".format(s, f))

    def list_transitions(self):
        print("FST has {} strings".format(self.chars))
        for t in self.transitions:
            t.print_trans()

    def print_fst_info(self):
        print ("Composed FST has total of {} states, {} transitions".format(len(self.states), len(self.transitions)))

    def reconstruct_upper(self, s):
        self.__reconstruct_u(s, "", "", "1")

    def reconstruct_lower(self, s):
        self.__reconstruct_l(s, "", "", "1")

    def __reconstruct_u(self, word, lower, upper, state):
        if lower == "@@" and self.states[state] is True:
            print upper
        elif lower == "@@" and self.states[state] is False:
            return
        else:
            for trans in self.transitions:
                if trans.source == str(state) and (word.startswith(lower + trans.lower) and word != lower + trans.lower):
                    self.__reconstruct_u(word, lower+trans.lower, upper+trans.upper, trans.dest)
                elif trans.source == str(state) and word == lower+trans.lower:
                    self.__reconstruct_u(word, "@@", upper+trans.upper, trans.dest)
            return

    def __reconstruct_l(self, word, upper, lower, state):
        if upper == "@@" and self.states[state] is True:
            print lower
        elif upper == "@@" and self.states[state] is False:
            return
        else:
            for trans in self.transitions:
                if trans.source == str(state) and (word.startswith(upper + trans.upper) and word != upper + trans.upper):
                    self.__reconstruct_l(word, upper+trans.upper, lower+trans.lower, trans.dest)
                elif trans.source == str(state) and word == upper+trans.upper:
                    self.__reconstruct_l(word, "@@", lower+trans.lower, trans.dest)
            return


class Transition:

    def __init__(self, s, l, u, d):
        self.source = s
        self.lower = l
        self.upper = u
        self.dest = d

    def print_trans(self):
        print("source: {}, lower: {}, upper: {}, dest: {}"
              .format(self.source, self.lower, self.upper, self.dest))
