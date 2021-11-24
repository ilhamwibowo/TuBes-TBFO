import os
import sys

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
    all_lines = list()
    res = list()
    file = ''.join(removecomment(open(filename, "r").read()))
    file1 = open("temp","w"); file1.write(file); file1.close()
    with open('temp', "r") as file:
        for line in file.readlines():
        
            # remove \n
            temp = " ".join(line[:-1].split())
            if (not(temp.startswith("#"))):
                res.append(temp)
        for i in range (len(res)):
            if (res[i] != ''):
                all_lines.append(res[i])
    
    """
    print('\nALL_LINES\n')
    print(all_lines)
    print('\n')
    """
    return all_lines

def removecomment(sentence):
    temp = sentence.split("\n")
    idxpetik = []
    for i in range(len(temp)):
        if "'''" in temp[i]:
            idxpetik.append(i)
    i = 0
    while (i < len(idxpetik)):
        try:
            for j in range(idxpetik[i],idxpetik[i+1]+1):
                temp[j] = ""
        except:
            for j in range(idxpetik[i],len(temp)):
                temp[j] = "^%"
        i += 2
    return '\n'.join(temp)

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
            tmp = len(te[1])
            if inp[i] == te[1][1:(tmp-1)]:
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
    # for c in inp:
    #     print("\t{}".format(c), end="\t")
    # print()
    # for i in range(len(inp)):
    #     print(i+1, end="")
    #     for c in tab[i]:
    #         if c == set():
    #             print("\t{}".format("_"), end="\t")
    #         else:
    #             print("\t{}".format(c), end=" ")
    #     print()

    if len(tab[len(inp)-1][0]) != 0:
        return True
    else:
        print("Syntax Error!")
        return False


if __name__ == '__main__':
    error = False
    grammar = "cnf.txt"
    inputan = str(sys.argv[1])
    v, t = read_grammar(grammar)
    inputlines = read_input(inputan)
    for lines in inputlines:
        lines = lines.replace(" ","")
        ta = cyk_alg(v, t, lines)
        show_result(ta, lines)
        if (error):
            break

    if (not error):
        print("Accepted!")
