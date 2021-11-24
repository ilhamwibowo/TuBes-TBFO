import sys
sys.setrecursionlimit(10000)

#insert new start symbol
def insert_new_start(cfg):
    string = "S0 -> S\n"
    cfg.insert(0,string)
    return cfg

#parse cfg per production rules line
def parse_prod(prod):
    x = list(filter(None,map(lambda x: x.replace(' ', '').replace('\n',''), prod.split(" "))))
    result = []
    if (len(x) == 2):
        for j in range(len(x)):
            found = False
            if (x[j][0] == "'"):
                for cnf in cnfs:
                    if (x[j] == cnf.split(" -> ")[1]):
                        found = True
                        x[j] = cnf.split(" ")[0]
                        break
                if not(found):
                    if (x[j][1:-1] == ""):
                        cnfs.append('A'+str(i[0])+" -> ' "+x[j][1:-1]+"'")
                        x[j] = 'A'+str(i[0])
                        it = i[0] + 1
                        i.pop(0)
                        i.append(it)
                    else :
                        cnfs.append('A'+str(i[0])+" -> '"+x[j][1:-1]+"'")
                        x[j] = 'A'+str(i[0])
                        it = i[0] + 1
                        i.pop(0)
                        i.append(it)
        result += [' '.join(x)]
    elif (len(x) == 1):
        if (not (x[0][0] == "'")):
            for j in range(len(cfgs)):
                if (cfgs[j].find(x[0]) == 0):
                    break
            desc = cfgs[j].split("->")
            symbol = desc[0]
            prods = desc[1].split("|")
            for prod in prods:
                result += parse_prod(prod)
        else:
            result += x
    else:
        for j in range(len(x)):
            found = False
            if (x[j][0] == "'"):
                for cnf in cnfs:
                    if (x[j] == cnf.split(" -> ")[1]):
                        found = True
                        x[j] = cnf.split(" ")[0]
                        break
                if not(found):
                    if (x[j][1:-1] == ""):
                        cnfs.append('A'+str(i[0])+" -> ' "+x[j][1:-1]+"'")
                        x[j] = 'A'+str(i[0])
                        it = i[0] + 1
                        i.pop(0)
                        i.append(it)
                    else :
                        cnfs.append('A'+str(i[0])+" -> '"+x[j][1:-1]+"'")
                        x[j] = 'A'+str(i[0])
                        it = i[0] + 1
                        i.pop(0)
                        i.append(it)
        result += [' '.join(eliminate_variables(x))]
    return result

#eliminate more than 2 variables
def eliminate_variables(prod):
    if (len(prod) > 2):
        found = False
        a = eliminate_variables(prod[1:])
        for cnf in cnfs:
            if (' '.join(a) == cnf.split(' -> ')[1]):
                found = True
                newVariable = cnf.split(' -> ')[0]
                break
        if not(found):
            newVariable = 'A' + str(i[0])
            it = i[0] + 1
            i.pop(0)
            i.append(it)
            res = a
            cnfs.append(newVariable+" -> "+res[0]+" "+res[1])
        return [prod[0], newVariable]
    else:
        return prod
        
#parse cfg per line 
def parse(cfg):
    cfglist = cfg.split("->")
    symbol = cfglist[0].replace(' ','')
    prods = cfglist[1].split("|")
    result = []
    for prod in prods:
        result += parse_prod(prod)
    return symbol + ' -> ' + ' | '.join(list(dict.fromkeys(result)))

def convertCFGtoCNF(filename):
    global cnfs
    global cfgs
    global i
    i =[0]
    cfgs = list(filter(None,map(lambda x: x.replace('\n','').replace('\r',''),open(filename,'r').readlines())))
    cnfs = []
    cnfs = [parse(cfgs[0])] + cnfs
    for cfg in cfgs[1:]:
        cnfs.append(parse(cfg))
    cnfs = list(map(lambda x: x+ '\n', cnfs))
    cnfs = insert_new_start(cnfs)
    open('cnf.txt','w').writelines(cnfs)


filename = input()
convertCFGtoCNF(filename)
