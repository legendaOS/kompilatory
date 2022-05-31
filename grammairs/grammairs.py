class Grammair:
    def __init__(self) -> None:
        self.Terminals = []
        self.NonTerminals = []
        self.Rules = []
        self.Start = None
        self.Epsilon = 'eps'
    
    def setTerminal(self, letter: str) -> None:
        self.Terminals.append(letter)
    
    def setNonTerminal(self, letter: str) -> None:
        self.NonTerminals.append(letter)
    
    def setStart(self, letter: str) -> None:
        self.Start = letter

    def setRule(self, LeftLetters: list, RightLetters: list) -> None:
        self.Rules.append([LeftLetters, RightLetters]) 

    def __str__(self) -> str:
        buf = ''
        buf += 'Terminals:\n'
        for letter in self.Terminals:
            buf += ' ' + letter
        buf += '\nNonterminals:\n'
        for letter in self.NonTerminals:
            buf += ' ' + letter
        buf += f'\nStart: {self.Start}\n'
        buf += 'Rules:\n'
        for rule in self.Rules:
            left = ''
            right = ''
            for letter in rule[0]:
                left += letter
            for letter in rule[1]:
                right += letter
            strbuf = f' {left} -> {right}'
            buf += strbuf + '\n'
        return buf




def findEpsGenerating(g: Grammair) -> list:
    # 1. Найти все ε-правила. Составить множество, состоящее из нетерминалов, входящих в левые части таких правил.
    # Правила вида A→ε называются ε-правилами (англ. ε-rule).

    epsGenerating = []

    for rule in g.Rules:
        if getRight(rule) == [g.Epsilon]:
            for letter in getLeft(rule):
                if letter in g.NonTerminals:
                    epsGenerating.append(letter)

    # 3. Если на шаге 2 множество изменилось, то повторить шаг 2.

    change = True
    while change:
        change = False

        # 2. Перебираем правила грамматики Γ. Если найдено правило A→C1C2…Ck, для которого верно, 
        # что каждый Ci принадлежит множеству, то добавить A в множество.

        for rule in g.Rules:
            flag = True
            
            for letter in getRight(rule):
                if not letter in epsGenerating:
                    flag = False

            if flag:
                l = getLeft(rule)[0]

                if not l in epsGenerating:
                    change = True
                    epsGenerating.append(l)

    return epsGenerating

#стремная магия

from itertools import chain, combinations

def powerset(iterable):
    # powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def magiclol(input_list):
    return list(map(list, powerset(input_list)))[1:]



# начало магии

def magicConvert(inp_list):

    k = magiclol(inp_list)

    buf = []
    buf.append([None for k in range(len(inp_list))])

    for element in k:
        microbuf = []
        for letter in inp_list:
            if letter in element:
                microbuf.append(letter)
            else:
                microbuf.append(None)
        buf.append(microbuf)
    
    return buf

#конец магии




    
def deleteEpsGenerating(g: Grammair):

    flagStartSymbToEps = False
    for rule in g.Rules:
        if getLeft(rule) == [g.Start] and getRight(rule) == [g.Epsilon]:
            flagStartSymbToEps = True 

    #1. Добавить все правила из P в P′.

    newRules = g.Rules.copy()

    #2. Найти все ε-порождаюшие нетерминалы.

    epsGenerating = findEpsGenerating(g)

    #3. Для каждого правила вида A→α0B1α1B2α2…Bkαk  (где αi — последовательности из терминалов и нетерминалов, 
    # Bj — ε-порождающие нетерминалы) добавить в P′ все возможные варианты правил, в которых либо присутствует, 
    # либо удалён каждый из нетерминалов Bj(1⩽j⩽k).

    for rule in g.Rules:

        epsGen = []
        pattern = []

        leftPart = getLeft(rule)

        for letter in getRight(rule):
            if not letter in epsGenerating:
                pattern.append([letter])
            else:
                pattern.append([])
                epsGen.append(letter)
        
        magicList = magicConvert(epsGen)

        for element in magicList:
            patternedBuf = []
            index = 0
            for inpattern in pattern:
                if inpattern == []:
                    if element[index] != None:
                        patternedBuf.append([element[index]])
                    else:
                        patternedBuf.append([])
                else:
                    patternedBuf.append(inpattern)
                index += 1

            rightPart = []
            for ii in patternedBuf:
                if ii != []:
                    rightPart.append(ii[0])
            
            bufnewrule = [leftPart, rightPart]

            if not bufnewrule in newRules and rightPart != []:
                newRules.append(bufnewrule)
        

    # 4. Удалить все ε-правила из P′.
    new_newRules = []
    for rule in newRules:
        if getRight(rule) != [g.Epsilon]:
            new_newRules.append(rule)

    
    #5. Если в исходной грамматике Γ выводилось ε, то необходимо добавить новый нетерминал S′, 
    # сделать его стартовым, добавить правило S′→S|ε.
                
    if flagStartSymbToEps:
        newStartLetter = g.Start + '`'
        newStartRule1 = [[newStartLetter], [g.Start]]
        newStartRule2 = [[newStartLetter], [g.Epsilon]]
        new_newRules.append(newStartRule1)
        new_newRules.append(newStartRule2)
        g.Start = newStartLetter
        g.NonTerminals.append(newStartLetter)

    # обновить правила в грамматике

    g.Rules = new_newRules

                

def findNonGenerating(g:Grammair):
    # Шаг 0. Множество порождающих нетерминалов пустое.
    generating = []


    # Шаг 1. Находим правила, не содержащие нетерминалов в правых частях и добавляем нетерминалы,
    # встречающихся в левых частях таких правил, в множество.

    for rule in g.Rules:
        flag = True
        for letter in getRight(rule):
            if letter in g.NonTerminals:
                flag = False
    
        if flag:
            for letter in getLeft(rule):
                generating.append(letter)

    # Шаг 2. Если найдено такое правило, что все нетерминалы, стоящие в его правой части, уже входят в множество, 
    # то добавим в множество нетерминалы, стоящие в его левой части.

    change = True
    while change:
        change = False

        for rule in g.Rules:

            
            flag = True
            for letter in getRight(rule):
                if letter in g.NonTerminals:
                    if not letter in generating:
                        flag = False
            if flag:
                for letter in getLeft(rule):
                    if letter in g.NonTerminals:
                        if not letter in generating:
                            generating.append(letter)
                            change = True

    # Шаг 3. Повторим предыдущий шаг, если множество порождающих нетерминалов изменилось.



    #В результате получаем множество всех порождающих нетерминалов грамматики, а все нетерминалы, 
    # не попавшие в него, являются непорождающими.
        
    nonGener = []

    for letter in g.NonTerminals:
        if not letter in generating:
            nonGener.append(letter)

    return nonGener


def findUnreachable(g: Grammair):
    #Шаг 0. Множество достижимых нетерминалов состоит из единственного элемента: {S}.

    reachable = [g.Start]

    #Шаг 1. Если найдено правило, в левой части которого стоит нетерминал, содержащийся в множестве, 
    # добавим в множество все нетерминалы из правой части.

    change = True
    while change:
        change = False

        for rule in g.Rules:
            flag = False
            for letter in getLeft(rule):
                if letter in reachable:
                    flag = True
            if flag:
                for letter in getRight(rule):
                    if letter in g.NonTerminals:
                        if not letter in reachable:
                            reachable.append(letter)
                            change = True

    # Шаг 2. Повторим предыдущий шаг, если множество порождающих нетерминалов изменилось.

    # Получаем множество всех достижимых нетерминалов, а нетерминалы, не попавшие в него, являются недостижимыми.

    unreachable = []
    for letter in g.NonTerminals:
        if not letter in reachable:
            unreachable.append(letter)

    return unreachable


def deleteUseless(g:Grammair):

    # Удалить из грамматики правила, содержащие непорождающие нетерминалы.

    nonGen = findNonGenerating(g)

    newRules = []
    newNonTerms = []

    for rule in g.Rules:
        flag = False
        for letter in getRight(rule):
            if letter in nonGen:
                flag = True
        for letter in getLeft(rule):
            if letter in nonGen:
                flag = True
        if not flag:
            if not rule in newRules:
                newRules.append(rule)

    for letter in g.NonTerminals:
        if not letter in nonGen:
            if not letter in newNonTerms:
                newNonTerms.append(letter)

    g.NonTerminals = newNonTerms
    g.Rules = newRules

    #Удалить из грамматики правила, содержащие недостижимые нетерминалы.

    nonGen = findUnreachable(g)

    newRules = []
    newNonTerms = []

    for rule in g.Rules:
        flag = False
        for letter in getRight(rule):
            if letter in nonGen:
                flag = True
        for letter in getLeft(rule):
            if letter in nonGen:
                flag = True
        if not flag:
            if not rule in newRules:
                newRules.append(rule)

    for letter in g.NonTerminals:
        if not letter in nonGen:
            if not letter in newNonTerms:
                newNonTerms.append(letter)

    g.NonTerminals = newNonTerms
    g.Rules = newRules
        

def deleteLeftRecursion(g: Grammair, Ai):
    """
        Удаляет непосредственную левую рекурсию из грамматики g для символа Ai
    """


    A = g.NonTerminals.copy()
    index = A.index(Ai)

    B = A[index]
    A = [B]

    toDeleteRules = []
    toAddRules = []
    toAddNonTerminals = []

    RULES = g.Rules.copy()

    for i in range(len(A)):

        # устранить непосредственную левую рекурсию

        flagToRecursionForward = False

        bufToAppendRules = []
        bufToDeleteRules = []

        newShtrish = A[i] + '`'


        for rule in RULES: 
            if getLeft(rule)[0] == A[i]:

                if getRight(rule)[0] == A[i]:
                    flagToRecursionForward = True #есть хотябы одно леворекурсивное правило

                    # Собрать правила из A[i] -> A[i]alpha[1]|...|A[i]alpha[n]
                    # Такого вида: 1) A[i]` -> alpha[1]A[i]`|...|alpha[n]A[i]`
                    #              2) A[i]` -> alpha[1]|...|alpha[i]

                    if not rule in bufToDeleteRules:
                        bufToDeleteRules.append(rule)

                    newRuleBuf1 = [[newShtrish]]
                    newRuleBuf2 = [[newShtrish]]

                    alphaBuf = getRight(rule)[1:len(getRight(rule))]

                    rbuf = []
                    for lettr in alphaBuf: rbuf.append(lettr)

                    if rbuf != [g.Epsilon]:
                        rbuf.append(newShtrish)
                        newRuleBuf1.append(rbuf)
                        newRuleBuf2.append(alphaBuf)
                        if not newRuleBuf1 in bufToAppendRules:
                            bufToAppendRules.append(newRuleBuf1)
                        if not newRuleBuf2 in bufToAppendRules:
                            bufToAppendRules.append(newRuleBuf2)

                else:

                    # собрать правила из A[i] -> betta[1]|...|betta[m]
                    # Вида 1) A[i] -> betta[1]A[i]`|...|betta[m]A[i]`
                    #      2) A[i] -> betta[1]|...|betta[m]

                    if not rule in bufToDeleteRules:
                        bufToDeleteRules.append(rule)

                    newRuleBuf1 = [[A[i]]]
                    newRuleBuf2 = [[A[i]]]

                    bettaBuf = getRight(rule)

                    rbuf = []
                    for lettr in bettaBuf: rbuf.append(lettr)
                    rbuf.append(newShtrish)

                    newRuleBuf1.append(rbuf)
                    newRuleBuf2.append(bettaBuf)

                    if not newRuleBuf1 in bufToAppendRules:
                            bufToAppendRules.append(newRuleBuf1)
                    if not newRuleBuf2 in bufToAppendRules:
                        bufToAppendRules.append(newRuleBuf2)
                    
        # добавим правила если была хоть одна леворекурсивная продукция

        if flagToRecursionForward:
            #добавим новый нетерминал 
            toAddNonTerminals.append(newShtrish)

            for microRule in bufToAppendRules:
                if not microRule in toAddRules:
                    toAddRules.append(microRule)
            
            for microRule in bufToDeleteRules:
                if not microRule in toDeleteRules:
                    toDeleteRules.append(microRule)


            
                

    newRules = []
    for rule in g.Rules:
        if not rule in toDeleteRules:
            newRules.append(rule)

    for rule in toAddRules:
        if not rule in newRules:
            newRules.append(rule)

    g.Rules = newRules

    for newNonTermMicro in toAddNonTerminals:
        g.NonTerminals.append(newNonTermMicro)




def deleteAllLeftRecursion(g: Grammair):
    """
        Устраняет произвольную левую рекурсию из грамматики g
    """

    A = g.NonTerminals.copy()

    for i in range(len(A)):

        toDeleteRules = []
        toAddRules = []

        for j in range(i):
            
            for rule in g.Rules:
                # Для каждого правила вида A[i] -> A[j]gamma
                # Удалить такое правило

                if getLeft(rule)[0] == A[i] and getRight(rule)[0] == A[j]:
                    if not rule in toDeleteRules:
                        toDeleteRules.append(rule)

                bufGamma = []
                r = getRight(rule)[1: len(getRight(rule))]
                for lettr in r:
                    bufGamma.append(lettr)

                # Для каждого праивла вида Q -> x[i] из правил вида A[j] -> delta[i]
                # Добавть правило вида A[i] -> x[i]gamma

                for microRule in g.Rules:
                    if getLeft(microRule)[0] == A[j]:
                        bufDelta = getRight(microRule)
                        bufToNewRule = bufDelta.copy()
                        for lettr in bufGamma:
                            bufToNewRule.append(lettr)


                        if not [[A[i]], bufToNewRule] in toAddRules:
                            toAddRules.append([[A[i]], bufToNewRule])

            # Добавить и удалить полученные правила
                new_Rules = []
                for microRule in g.Rules:
                    if not microRule in toDeleteRules:
                        new_Rules.append(microRule)

                for microRule in toAddRules:
                    if not microRule in new_Rules:
                        new_Rules.append(microRule)

            # Устранить непосредственную левую рекурсию для символа A[i]
            deleteLeftRecursion(g, A[i])
                        






def fillGrammair(G: Grammair, Terms: list, NonTerms: list, Start: str, Rules: list) -> None:
    for letter in Terms:
        G.setTerminal(letter)
    for letter in NonTerms:
        G.setNonTerminal(letter)
    G.setStart(Start)
    for rule in Rules:
        G.setRule(rule[0], rule[1])


def getLeft(rule: list) -> list:
    return rule[0]
def getRight(rule: list) -> list:
    return rule[1]



# g = Grammair()

# t = 'a,b,y'.split(',')
# n = 'A,S'.split(',')
# s = 'S'
# r = [
#     [['A'], ['S','a']],
#     [['S'], ['S','b']],
#     [['S'], ['A','y']],
#     [['S'], ['b']]
# ]





# fillGrammair(g, t, n, s, r)

# print(g)
# print('---------------------------')

# deleteAllLeftRecursion(g)
# print(g)