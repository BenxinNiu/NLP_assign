class CKY:

    def __init__(self, rules, non_terminals):
        self.rules = rules
        self.non_terminals = list(non_terminals)
        self.p = list()

    def b2_bomber(self, words):
        assert type(words) is list
        self.__get_empty_matrix(words)
        self.__fill_in_base_single_word(words)
        self.__fill_in_remaining_case(words)
        # self.__print_matrix()
        return self.p

    def __fill_in_base_single_word(self, words):
        matrix_length = len(self.p)
        for j in range(1, matrix_length):
            for rule in self.rules:
                self.__try_append(j, rule, words[j])
            self.__resolve_unary(j)

    def __fill_in_remaining_case(self, words):
        matrix_length = len(self.p)
        for j in range(2, matrix_length):
            for i in range(j-2, 0 -1, -1):
                self.__apply(i, j)

    def __apply(self, i, j):
        for k in range(i+1, j):  # for k = i +1 to j-1 do:
            for r in self.rules:
                if len(r) >= 3 and len(self.p[i][k][r[1]]) != 0 and len(self.p[k][j][r[2]]) != 0:
                    self.p[i][j][r[0]].append([k, r])
        self.__resolve_unary_two(i, j)

    def __resolve_unary_two(self, i, j):
        change = True
        while change:
            change = False
            for t in self.non_terminals:
                bool_unary, rule = self.__check_unary(t)
                if len(self.p[i][j][t]) != 0 and bool_unary:
                    tmp = [j, rule]
                    if not (tmp in self.p[i][j][rule[0]]):
                        self.p[i][j][rule[0]].append(tmp)
                        change = True

    def __resolve_unary(self, j):
        change = True
        while change:
            change = False
            for t in self.non_terminals:
                bool_unary, rule = self.__check_unary(t)
                if len(self.p[j - 1][j][t]) != 0 and bool_unary:
                    tmp = [j, rule]
                    if not (tmp in self.p[j - 1][j][rule[0]]):
                        self.p[j - 1][j][rule[0]].append(tmp)
                        change = True

    def __check_unary(self, N):
        assert type(self.rules) is list
        assert type(N) is str
        for r in self.rules:
            if len(r) == 2 and N == r[1]:
                return True, r
        return False, []

    def __try_append(self, j, rule, w):
        assert type(w) is str
        if w == rule[1]:
            tmp = [j, rule]
            self.p[j-1][j][rule[0]].append(tmp)

    def __get_empty_matrix(self, words):
        matrix_length = len(words)
        for i in range(0, matrix_length):
            tmp = []
            for j in range(0, matrix_length):
                tmp.append(None)
            self.p.append(tmp)
        for j in range(1, matrix_length):
            for i in range(0, j):
                tmp = dict()
                for t in self.non_terminals:
                    tmp[t] = list()
                self.p[i][j] = tmp

    def __print_matrix(self):
        for i in self.p:
            for j in i:
                print j
            print "\n"