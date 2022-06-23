from grammairs import Grammair, fillGrammair, getLeft, getRight

t = ['+', '*', ')', '(', 'a']
n = ['E']
s = 'E'
p = [
    [['E'], ['E' , '+' ,'E']],
    [['E'], ['E' , '*' ,'E']],
    [['E'], ['(', 'E', ')']],
    [['E'], ['a']]
]

g = Grammair()
fillGrammair(g, t, n, s, p)

from prettytable import PrettyTable

def printTable(tbl):
    rtable = PrettyTable()

    names = []

    for i in tbl[list(tbl.keys())[0]]:
        names.append(i)
        1+1

    bnames = ['']
    bnames.extend(names)

    rtable.field_names = bnames

    superbuf = []

    for letter in tbl:
        buf = [letter]
        lol = list(tbl[letter].keys())
        if lol != names:
            raise Exception('Неверный формат таблицы')
        for microletter in tbl[letter]:
            buf.append(tbl[letter][microletter])
        superbuf.append(buf)

    rtable.add_rows(superbuf)
    

    print(rtable)

    

table = {
    ')': {'(':'Err', 'a': 'Err', '*':'>', '+':'>', ')':'>', '$': '>'},
    'a': {'(':'Err', 'a': 'Err', '*':'>', '+':'>', ')':'>', '$': '>'},
    '*': {'(':'<', 'a': '<', '*':'>', '+':'>', ')':'>', '$': '>'},
    '+': {'(':'<', 'a': '<', '*':'<', '+':'>', ')':'>', '$': '>'},
    '(': {'(':'<', 'a': '<', '*':'<', '+':'<', ')':'=', '$': 'Err'},
    '$': {'(':'<', 'a': '<', '*':'<', '+':'<', ')':'Err', '$': 'Accept'},
}

print(g)
printTable(table)



def findLastTerm(toks:list, terms:list):
    for i in range(len(toks) - 1, -1, -1):
        if toks[i] in terms:
            return toks[i]
    

def OPP(tokens: list, g:Grammair, table:list, debugFlag = True):
    MyStack = ['$']
    CurTokens = tokens.copy()

    terms = g.Terminals
    terms.append('$')

    retRules = []

    nowDo = ''

    while True:
        if debugFlag:
            mbfstck = MyStack.copy()
            tknsbf = CurTokens.copy()

        rightTerm = findLastTerm(MyStack, terms)
        tableElement = table[rightTerm][CurTokens[0]]

        if tableElement == 'Err':
            raise Exception(f'Ошибка для пары токенов {rightTerm} {CurTokens[0]}')

        elif tableElement in ['<', '=']:
            nowDo = f'shift {CurTokens[0]}'
            MyStack.append(CurTokens.pop(0))

        elif tableElement == '>':
            poppedBuffer = []
            latest = None

            #попать все до первого терминала и его тоже
            while True:
                index = len(MyStack) - 1

                if index < 1: raise Exception('что-то пошло не так')

                if MyStack[index] in terms:
                    #сделать его крайним
                    latest = MyStack[index]

                    poppedBuffer.append(MyStack.pop())
                    break
                else:
                    poppedBuffer.append(MyStack.pop())

            #попать до следующего терминала пока не появится < между ним и текущим крайним

            while True:
                index = len(MyStack) - 1

                if index < 0: raise Exception('что-то пошло не так')

                if MyStack[index] in terms:
                    #нашли следущий терминал

                    if table[MyStack[index]][latest] == '<':
                        #нашли reduce
                        break
                    else:
                        #не нашли reduce
                        # сделать его крайним
                        # и попнуть его
                        latest = MyStack[index] 
                        poppedBuffer.append(MyStack.pop())
                else:
                    poppedBuffer.append(MyStack.pop())

            realPopBuf = poppedBuffer[::-1]

            #поиск правила в грамматике у которого правая часть это то что попнули

            appendedNT = None

            for rule in g.Rules:
                rpart = getRight(rule)
                if rpart == realPopBuf:
                    #нашли
                    appendedNT = getLeft(rule)[0]
                    retRules.append(rule)
                    break
                # не нашли
            if not appendedNT:
                raise Exception(f'правило с правой частью {realPopBuf} не найдено')
            
            MyStack.append(appendedNT)

            nowDo = f'reduce {getLeft(retRules[-1])[0]} -> {str(getRight(retRules[-1]))}'
            1+1



        elif tableElement == 'Accept':
            if MyStack[-1] == g.Start:
                nowDo = 'Accepted'
                print(f'Stack: {mbfstck} | tokens: {tknsbf} | {nowDo}')
                return retRules
            else:
                nowDo = 'Symbol is not Start'
                print(f'Stack: {mbfstck} | tokens: {tknsbf} | {nowDo}')
                raise Exception('неверный конец разбора')

        else:
            raise Exception('неверный символ в таблице')
        
        if debugFlag:
            print(f'Stack: {mbfstck} | tokens: {tknsbf} | {nowDo}\n')


tokenses = '( a + a ) + ( a + a ) * ( a + a ) $'.split(' ')

print(f'Разбор строки {tokenses}\n')

RulesToCreateTree = OPP(tokenses, g, table)

print('правила получены')


print('строим дерево')

from ATLcreate import ATLTree, ATLNode, Rs, Shstr

def createTreeFromRules(RulesToCreateTree: list, g:Grammair) -> ATLTree:

    NodeStack = []

    for rule in RulesToCreateTree:
        RightPart = getRight(rule)
        NodeName = getLeft(rule)[0]



        if all([i in g.Terminals for i in RightPart]):
            #если все символы правой части правила
            #терминалы, то построить новую вершину
            #и засунуть ее в стек вершин

            bufChildrens = []

            for letter in RightPart:
                #для каждого терминала правой части сделать ноду
                bufNode = ATLNode('T', letter)
                bufChildrens.append(bufNode)
            
            bufNoda = ATLNode('N', NodeName)
            bufNoda.AddChildrens(bufChildrens)

            NodeStack.append(bufNoda)

        
        else:
            #если в правой части есть нетерминалы, то надо
            #по очереди либо создавать ноду для терминала
            #либо приделывать к новой ноде детей с верхушки стека созданых нод

            bufChildrens = []

            #получить нетерменальные ноды в нужном порядке

            bufNonTNodes = []

            count = 0
            for i in RightPart:
                if i in g.NonTerminals:
                    count += 1

            for i in range(count):
                bufNonTNodes.append(NodeStack.pop())

            

            for letter in RightPart:
                if letter in g.Terminals:
                    bufNode = ATLNode('T', letter)
                    bufChildrens.append(bufNode)
                else:
                    bufChildrens.append(bufNonTNodes.pop())

            bufNoda = ATLNode('N', NodeName)

            bufNoda.AddChildrens(bufChildrens)

            NodeStack.append(bufNoda)


    retTree = ATLTree()
    retTree.Root = NodeStack[0]

    return retTree   


MyTree = createTreeFromRules(RulesToCreateTree, g)
print('дерево построено')

MyTree.printTree()

print(Rs(MyTree.Root, g))

print('перевод в обратную польскую')

def ParceTreePoland(t: ATLTree) -> list:
    res = []
    allNodes = Shstr(t.Root)

    for noda in allNodes:
        NType = noda.TypeElement
        Letter = noda.Letter

        if NType == 'T':
            res.append(Letter)

        else:
            LENG = len(noda.Childrens)
            buf = []
            for i in range(LENG):
                buf.append(res.pop())
            
            rightBuf = buf[::-1]


            if LENG > 1:

                if rightBuf[0] == '(':
                    res.append(f'{rightBuf[1]}')
                else:
                    res.append(f'{rightBuf[1]}{rightBuf[0]}{rightBuf[2]}')

            else:
                res.append(rightBuf[0])

    return res[0]




stoka = ParceTreePoland(MyTree)
print(stoka)