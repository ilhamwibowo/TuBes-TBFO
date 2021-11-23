
import sys
sys.setrecursionlimit(100000)
print(sys.getrecursionlimit())

def eliminateTwoVariables(prod):
    if (len(prod) > 2):
        found = False
        a = eliminateTwoVariables(prod[1:])
        for cnf in cnfs:
            if (' '.join(a) == cnf.split(' -> ')[1]):
                found = True
                newvar = cnf.split(' -> ')[0]
                break
        if not(found):
            newvar = 'A' + str(i[0])
            it = i[0] + 1
            i.pop(0)
            i.append(it)
            res = a
            cnfs.append(newvar+" -> "+res[0]+" "+res[1])
        return [prod[0], newvar]
    else:
        return prod

#parse cfg per production rules line
def parsing_cfg_prod(prod):
    x = list(filter(None,map(lambda x: x.replace(' ', '').replace('\n',''), prod.split(" "))))
    result = []
    if (len(x) == 2):
        for j in range(len(x)):
            found = False
            if (x[j][0].islower()):
                for cnf in cnfs:
                    if (x[j] == cnf.split(" -> ")[1]):
                        found = True
                        x[j] = cnf.split(" ")[0]
                        break
                if not(found):
                    cnfs.append('A'+str(i[0])+" -> "+x[j])
                    x[j] = 'A'+str(i[0])
                    it = i[0] + 1
                    i.pop(0)
                    i.append(it)
        result += [' '.join(x)]
    elif (len(x) == 1):
        if (not (x[0][0].islower())):
            for j in range(len(cfgs)):
                if (cfgs[j].find(x[0]) == 0):
                    break
            desc = cfgs[j].split("->")
            symbol = desc[0]
            prods = desc[1].split("|")
            for prod in prods:
                result += parsing_cfg_prod(prod)
        else:
            result += x
    else:
        for j in range(len(x)):
            found = False
            if (x[j][0].islower()):
                for cnf in cnfs:
                    if (x[j] == cnf.split(" -> ")[1]):
                        found = True
                        x[j] = cnf.split(" ")[0]
                        break
                if not(found):
                    cnfs.append('A'+str(i[0])+" -> "+x[j])
                    x[j] = 'A'+str(i[0])
                    it = i[0] + 1
                    i.pop(0)
                    i.append(it)
        result += [' '.join(eliminateTwoVariables(x))]
    return result

#parse cfg per line 
def parsing_cfg(cfg):
    desc = cfg.split("->")
    print(desc)
    symbol = desc[0].replace(' ','')
    prods = desc[1].split("|")
    result = []
    print(prods)
    for prod in prods:
        result += parsing_cfg_prod(prod)
    return symbol + ' -> ' + ' | '.join(list(dict.fromkeys(result)))

def remove_epsilon_rec(symbol, x, prods2):
    if (x != []):
        z = 0
        a = x.copy()
        while (z < len(a)):
            if (a[z] == symbol):
                a.pop(z)
                prods2 = remove_epsilon_rec(symbol, a, prods2)
                prods2.append(' '.join(a))
                a = a[:z] + [symbol]  + a[z:] 
            z += 1
    return prods2

def remove_epsilon(cfg):
    desc = cfg.split("->")
    symbol = desc[0].replace(' ','')
    prods = list(map(lambda x: x.replace('\n', '').replace('\r',''), desc[1].split("|")))
    for j in range(len(prods)):
        if ('EPSILON' in prods[j]):
            break
    prods.pop(j)
    cfgs[cfgs.index(cfg)] = symbol + ' -> ' + ' | '.join(list(dict.fromkeys(prods)))
    for j in range(len(cfgs)):
        if (symbol in cfgs[j]):
            desc = cfgs[j].split("->")
            symbol2 = desc[0].replace(' ','')
            prods2 = list(map(lambda x: x.replace('\n', '').replace('\r',''), desc[1].split("|")))
            for k in range(len(prods2)):
                if (symbol in prods2[k]):
                    x = list(filter(None,map(lambda x: x.replace(' ', '').replace('\n',''), prods2[k].split(" "))))
                    if (len(x) > 1):
                        z = 0
                        a = x.copy()
                        while (z < len(a)):
                            if (a[z] == symbol):
                                a.pop(z)
                                prods2 = remove_epsilon_rec(symbol, a, prods2)
                                prods2.append(' '.join(a))
                                a = a[:z] + [symbol] + a[z:] 
                            z += 1
                        cfgs[j] = symbol2 + ' -> ' + ' | '.join(list(dict.fromkeys(prods2)))
                    else:
                        prods2.append('EPSILON')
                        for z in range(len(prods2)):
                            if (symbol in prods2[z] and len(list(filter(None,prods2[z].split(" ")))) == 1):
                                break
                        prods2.pop(z)
                        cfgs[j] = symbol2 + ' -> ' + ' | '.join(list(dict.fromkeys(prods2)))
                        remove_epsilon(cfgs[j])

def searchSymbol(symbol, cfg, visited):
    if (' '+symbol in cfg):
        return True
    elif (len(visited) == len(cfgs)):
        return False
    else:
        cfglist = cfg.split("->")
        symbol2 = cfglist[0].replace(' ','')
        prods2 = list(map(lambda x: x.replace('\n', '').replace('\r','').split(' '), cfglist[1].split("|")))
        variabelList = list(dict.fromkeys(filter(None, map(lambda x: x.replace(' ',''), [k for j in prods2 for k in j]))))
        
        for j in variabelList:
            if (j.islower()):
                variabelList.remove(j)
        
        found = False
        for var in variabelList:
            if (found):
                break
            if (var != symbol2):
                for cfg2 in cfgs:
                    if (cfg2.split("->")[0].replace(' ','').replace('\n','') == var and not(cfg2 in visited)):
                        found = searchSymbol(symbol,cfg2,visited+[cfg2])
                        break
        return found

def remove_null(cfg):
    cfglist = cfg.split("->")
    symbol = cfglist[0].replace(' ','')
    found = searchSymbol(symbol, cfgs[0],[cfgs[0]])
    if not(found):
        j = cfgs.index(cfg)
        cfgs.pop(j)

def convertCFGtoCNF(filename):
    global cnfs
    global cfgs
    global i
    i =[0]
    cfgs = list(filter(None,map(lambda x: x.replace('\n','').replace('\r',''),open(filename,'r').readlines())))
    cnfs = []
    for cfg in cfgs:
        if ('EPSILON' in cfg):
            remove_epsilon(cfg)

    print(cfgs[0])
    cnfs = [parsing_cfg(cfgs[0])] + cnfs
    for cfg in cfgs[1:]:
        remove_null(cfg)
        cnfs.append(parsing_cfg(cfg))
    cnfs = list(map(lambda x: x+ '\n', cnfs))
    print(cnfs)


filename = input()
convertCFGtoCNF(filename)
