import os
import tokenize

def convert_to_token(filename):
    with tokenize.open(filename) as f:
        tokens = tokenize.generate_tokens(f.readline)
        all_lines = list()
        res = list()
        for token in tokens:
            if (token.type == 4):
                for i in range (len(res)):
                    all_lines.append(res[i])
                res = list()
            if (token.type != 4 and token.type != 5 and token.type !=6):
                res.append(token.string)
            print(token)
        print(all_lines)
    return all_lines


def create_cell(first, second):
    """
    creates set of string from concatenation of each character in first
    to each character in second
    first: first set of characters
    second: second set of characters
    """
    res = set()
    if first == set() or second == set():
        return set()
    for f in first:
        for s in second:
            res.add(f + ' ' +  s)
    return res


def read_grammar(filename):
    """
    reads the rules of a context free grammar from a text file
    return two lists. v_rules lead to variables and t_rules lead to terminals.
    """
    filename = os.path.join(os.curdir, filename)
    with open(filename) as grammar:
        rules = grammar.readlines()
        v_rules = []
        t_rules = []

        for rule in rules:
            left, right = rule.split(" -> ")

            # for two or more results from a variable
            right = right[:-1].split(" | ")
            for ri in right:
                
                # it is a variable
                if (str.isupper(ri)) and (ri[0] != "'"):
                    v_rules.append([left, ri])

                # it is a terminal
                else:
                    t_rules.append([left, ri])
        
        '''
        print('RULESSS\n')
        print(v_rules, t_rules)
        print('\n')
        '''
        return v_rules, t_rules


def read_input(filename):
    """
    reads the inputs from a text file
    :param filename: name of the text file in current directory
    :return: list of inputs
    """
    # Read each word
    filename = os.path.join(os.curdir, filename)
    res = list()
    all_lines = list()
    with open(filename) as inp:
        inputs = inp.readlines()
        for i in inputs:
    
            # remove \n
            res.append(i[:-1])
        for i in range(len(res)):
            all_lines.append(res[i].split())
    '''
    ** Read each character **
    filename = os.path.join(os.curdir, filename)
    all_lines = list()
    with open(filename) as inp:
        inputs = inp.readlines()
        for i in inputs:

            # remove \n
            all_lines.append(i[:-1])
    '''
    print('ALL_LINES\n')
    print(all_lines)
    print('\n')
    return all_lines


def cyk_alg(varies, terms, inp):
    """
    varies: rules related to variables
    terms: rules related to terminals
    inp: input string
    """

    length = len(inp)
    var0 = [va[0] for va in varies]
    var1 = [va[1] for va in varies]

    # table on which we run the algorithm
    table = [[set() for _ in range(length-i)] for i in range(length)]

    # Fill in the first row
    for i in range(length):
        for te in terms:
            if inp[i] == te[1]:
                table[0][i].add(te[0])

    # Fill in the remaining element
    for i in range(1, length):
        for j in range(length - i):
            for k in range(i):
                row = create_cell(table[k][j], table[i-k-1][j+k+1])
                for ro in row:
                    for cek in range (len(var1)):
                        if var1[cek] == ro:
                            table[i][j].add(var0[cek])
            
    return table


def show_result(tab, inp):
    for c in inp:
        print("\t{}".format(c), end="\t")
    print()
    for i in range(len(inp)):
        print(i+1, end="")
        for c in tab[i]:
            if c == set():
                print("\t{}".format("_"), end="\t")
            else:
                print("\t{}".format(c), end=" ")
        print()

    if len(tab[len(inp)-1][0]) != 0:
        print("The input belongs to this context free grammar!")
    else:
        print("The input does not belong to this context free grammar!")


if __name__ == '__main__':
    grammar = input("Masukkan file grammar: ")
    inputan = input("Masukkan file input: ")
    #lines = convert_to_token(inputan)
    v, t = read_grammar(grammar)
    for lines in read_input(inputan):
        ta = cyk_alg(v, t, lines)
        show_result(ta, lines)
