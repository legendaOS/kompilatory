from grammairs import *
import pptree 

class ATLTree:
    def __init__(self) -> None:
        self.Root = None

    def printTree(self, flag = False, Current = None, Horizontal = True):

        Verticals = None
        PPVerticals = None

        if flag: #Dubug print tree
            Verticals = [self.Root]
            if self.Root == Current:
                PPVerticals = [pptree.Node(f'>{self.Root.Letter}<:{self.Root.CurInd}')]
            else:
                PPVerticals = [pptree.Node(self.Root.Letter)]
            index = 0

            while True:
                bufChildrens = Verticals[index].Childrens.copy()
                for children in bufChildrens[-1::-1]:
                    Verticals.append(children)
                    if children == Current:
                        PPVerticals.append(pptree.Node(f'>{children.Letter}<:{children.CurInd}', PPVerticals[index]))
                    else:
                        PPVerticals.append(pptree.Node(f'{children.Letter}:{children.CurInd}', PPVerticals[index]))


                
                index += 1
                if index == len(Verticals): break

        else:
            Verticals = [self.Root]
            PPVerticals = [pptree.Node(self.Root.Letter)]
            index = 0

            while True:
                bufChildrens = Verticals[index].Childrens.copy()
                for children in bufChildrens[-1::-1]:
                    Verticals.append(children)
                    PPVerticals.append(pptree.Node(children.Letter, PPVerticals[index]))


                
                index += 1
                if index == len(Verticals): break

        pptree.print_tree(PPVerticals[0], horizontal = Horizontal)





class ATLNode:
    def __init__(self, stype, sletter) -> None:
        self.TypeElement = stype # 'N' - nonterminal \ 'T' - terminal
        self.Childrens = []
        self.Parent = None
        self.Letter = sletter
        self.Status = 'process' # ready
        self.Rules = []
        self.CurInd = None

    def AddChildrens(self, added):
        for elem in added:
            self.Childrens.append(elem)

    def clearChildrens(self):
        self.Childrens = []

    def changeStatus(self, sstatus):
        self.Status = sstatus


def Rstr(BufferRoot):
    """
    Обход вглубину
    """
    ret = []
    count = 0
    for element in BufferRoot.Childrens:
        if count == 1:
            ret.append(BufferRoot)
        for i in Rstr(element): 
            ret.append(i)
        count += 1
    
    if not BufferRoot in ret: ret.append(BufferRoot)
    return ret

def Rs(root: ATLNode, g:Grammair):
    """
    Вернет все терминалы в дереве слева направо
    """
    buf = Rstr(root)
    ret = []
    for i in buf:
        if i.Letter in g.Terminals:
            ret.append(i.Letter)
    return ret


def nextLeft(root, CurrentLeft, CGMAP):

    buf = Rstr(root)
    
    Nbuf = []
    for i in buf:
        if i.TypeElement == 'N':
            Nbuf.append(i)
    for k in Nbuf:
        if k.Status == 'process':
            if k != CurrentLeft:
                killChildrens(k)
                FillRules(k, CGMAP)
            return k
    return CurrentLeft

def findPRC(root):
    buf = Rstr(root)
    prc = 0
    for i in buf:
        if i.Status == 'process' and i.TypeElement == 'N':
            prc += 1

    return prc


def FillRules(CLeft: ATLNode, CGMAP):
    CLeft.Rules = CGMAP[CLeft.Letter].copy()

def parceLeft(CLeft: ATLNode, g:Grammair, CGMAP):
    letters = CLeft.Rules.pop()
    newNodes = []
    newNode = None
    for lettr in letters:
        if lettr in g.NonTerminals:
            newNode = ATLNode('N', lettr)
            newNode.Rules = CGMAP[lettr].copy()
        else:
            newNode = ATLNode('T', lettr)
        newNodes.append(newNode)
    
    CLeft.Childrens = newNodes.copy()
    CLeft.Status = 'ready'

def killChildrens(CLeft: ATLNode):
    CLeft.Childrens = []
    CLeft.Status = 'process'


def FindFather(CLeft, CRoot):
    #среди всех елементов выбрать тот у которого ребенок CLeft
    for element in Rstr(CRoot):
        if CLeft in element.Childrens:
            return element

def goPrevious(CLeft: ATLNode, CLeftStack, CGMAP, CRoot):

    counter = 0

    #если в списке разбираемых нод есть еще кто-то
    #обновить списокдоступных правил для текущей ноды
    #убить ее дете
    #перейти в предыдущую разбираемую ноду
    #если у нее еще есть правила для разбора, убить ее детей и удалить верхнее правило, вернуть ее из функции
    #если правил нет, то убить ее детей, обновить список доступных правил и отправиться дальше назад
    #если позадди никого нет,то это конец разбора, вернуть none

    

    Papa = FindFather(CLeft, CRoot)

    # if Papa == None:
    #     return None

    

    killChildrens(CLeft)
    FillRules(CLeft, CGMAP)
    if CLeft == CLeftStack[-1]: CLeftStack.pop()
    
    # if Papa != CLeftStack[-1]:
    #     FillRules(Papa, CGMAP)

    


    while True:
        
        if len(CLeftStack) > 0:
            counter += 1
            CLeft = CLeftStack.pop()
            1+1

            if len(CLeft.Rules) > 0:
                killChildrens(CLeft)

                if not CLeft in Rstr(Papa) or CLeft == Papa:
                    Papa.Childrens = []
                    Papa.Status = 'process'

                return CLeft


        else:
            return None

    #откатиться до разбираемого элемента с номером ind
    

def countCoincidence(ctokens, Rstokens):

    myTokens = Rstokens.copy()

    count = 0

    if len(myTokens) == 0:
        return count

    now = myTokens.pop(0)
    
    # for lettr in ctokens:

    #     if lettr == now:
    #         count += 1
    #         if len(myTokens) == 0:
    #             return count
    #         else:
    #             now = myTokens.pop(0)


    for lettr in ctokens:
        if now == lettr:
            count += 1
            if len(myTokens) == 0:
                return count
            else:
                now = myTokens.pop(0)
        else:
            return count
        

    return count
        




def LLRecursion(g:Grammair, tokens, debug = False) -> ATLTree:
    
    ind = 1

    GMAP = g.convertToDict()
    retTree = ATLTree()

    ROOT = ATLNode('N', g.Start)
    FillRules(ROOT, GMAP)
    ROOT.CurInd = ind

    retTree.Root = ROOT

    Left = ROOT
    LeftStack = []

    

    while True:

        RScount = countCoincidence(tokens, Rs(ROOT, g))

        if debug:
            print()
            retTree.printTree(flag=True, Current=Left)
            print()
            print('RScount', RScount, 'ind', ind)
            
            # print('RScount', RScount, 'ind', ind)
            
            print(Rs(ROOT, g))
            print(tokens)

            # lols = ''
            # lollen = 0
            # for loli in Rstr(ROOT): 
            #     lols += f'<{loli.Letter}>'
            #     lollen += 1
            # print(lols, lollen)

        bufRSlen = len(Rs(ROOT, g))

        # if bufRSlen > ind:
        #     ind += 1
        #     continue

        if bufRSlen > len(tokens):
            #длина разбора больше 
            # Удалить детей и верхнее правило или Идти назад по разбираемым верщинам в поиске той
            # у которой еще есть правила для разбора
            # У нее убить детей , дропнуть последнее разобранное правило
            # И сделать ее неразобранной
            
            if len(Left.Rules) > 0:
                #Если есть еще правило
                killChildrens(Left)

            else:
                #сделать Left неразобранным, обновить его
                # и искать предыдущий left который можно еще как-то разобрать
                # убить его детей и дропнуть верхнее правило
                killChildrens(Left)
                FillRules(Left, GMAP)
                Left = goPrevious(Left, LeftStack, GMAP, ROOT)
                if Left == None: return None
                ind = Left.CurInd
    

        #разбор несошелся
        if ( RScount < ind and RScount != len(tokens) ) or processFlag:
            processFlag = False

            #если можно разобрать текущю вершину
            if Left.Status == 'process':

                #раскрыть Left по верхнему правилу из ее доступных (там точно есть правила, ведь мы ее только добавили)
                parceLeft(Left, g, GMAP)
                Left.Status = 'ready'
                Left.CurInd = ind

                continue

            #если текущая вершина уже разобрана
            else:
                #Левый ребенок не разобран?
                if Left.Childrens[0].Status == 'process' and Left.Childrens[0].TypeElement == 'N':
                    
                    #Заносим текущую вершину в стек разбора
                    #и делаем левого ребенка текущим Left
                    Left.Status = 'ready'
                    LeftStack.append(Left)
                    Left = Left.Childrens[0]

                    #смотрим дальше 
                    # if ind != 1:
                    #     ind -= 1
                    continue

                #нет левого ребенка для разбора 
                else:

                    #попытаемся разобрать как-то по-другому, или переходить к родителям
                    #пока не сможем разобрать как-то по-другому их
                    #если разбирать как-то по-другому некого, то это - ошибка

                    if len(Left.Rules)>0:
                        #если еще есть правила, убить детей и дропнуть верхнее правило
                        killChildrens(Left)
                        #Left.Rules.pop()
                        1+1
                    else:
                        # парвил нет, переходим на предыдущее правило которое можно исправить
                        Left = goPrevious(Left, LeftStack, GMAP, ROOT)
                        if Left == None: return None
                        ind = Left.CurInd
                        1+1
                    if Left == None: # если перейти неудалось то все
                        return None

                    #идем дальше 
                    # if ind != 1:
                    #     ind -= 1
                    continue

        else:
            #разбор сходится до ind символа

            #Left меняется на следующий неразобраный левый нетерменал, увеличиваем совпадающую строку
            
            

            ind += 1


            #если проверена всетокены
            if ind == len(tokens) + 1:

                #если больше нет неразобранных нетерменалов
                #то все
                prc = findPRC(ROOT)
                if prc == 0:
                    return retTree

                #Если есть неразобранный нетерминал, то падаем в обратно в разбор
                else:
                    processFlag = True
                    

            #продолжить разбор

            if not Left in LeftStack:
                LeftStack.append(Left)

            if RScount >= ind - 1:
                Left = nextLeft(ROOT, Left, GMAP) 

            continue





def createATLbyLL(g: Grammair, tokens: list, debug = False) -> ATLTree:
    """
    Строит дерево разбора по грамматике g - Grammair по списку токенов tokens - list[str]
    """

    #получаем словарь возможных переходов для грамматики
    GMAP = g.convertToDict()
    GMAPold = g.convertToDict()

    retTree = ATLTree()
    
    #корнем дерева разбора является корень грамматики
    ROOT = ATLNode('N', g.Start)

    retTree.Root = ROOT


    #Текущий разбираемый символ - корень
    Left = ROOT
    LeftStack = []

    #Описание нод CV и списков их допускаемых переходов LP
    CV = {}
    LP = []

    ind = 1 # текущий индекс в списке токенов дод которого проверять идентичность с деревом
    prc = 1 # не разобранных вершин в текущий момент (корень не разобран - единственная вершина)

    while True:

        # if not GMAP == GMAPold:
        #     GMAP = g.convertToDict()

        RS = Rs(ROOT, g)

        if debug:
            retTree.printTree(flag=True, Current=Left)
            print(tokens)
            print(tokens[0: ind])
            print(RS)

        bufRSlen = len(RS)

        # Если длина текущего разбора больше длины цепочки токенов
        # Удалить детей и верхнее правило или Идти назад по разбираемым верщинам в поиске той
        # у которой еще есть правила для разбора
        # У нее убить детей , дропнуть последнее разобранное правило
        # И сделать ее неразобранной

        lenflag = False

        if bufRSlen >= len(tokens):
            lenflag = True

        if lenflag:
            if len(LP[CV[Left]]) > 1:
                #если еще есть правило на разбор
                Left.Childrens = []
                Left.Status = 'process'
                LP[CV[Left]].pop()

                ind = 1
                continue
            else:
                #сделать Left неразобранным, обновить его
                # и искать предыдущий left который можно еще как-то разобрать
                # убить его детей и дропнуть верхнее правило

                Left.Childrens = []
                Left.Status = 'process'
                LP[CV[Left]] = GMAP[Left.Letter].copy()

                retlenflag = True
                while retlenflag:
                    if len(LeftStack) > 1:
                        Left = LeftStack.pop()
                        
                        if len(LP[CV[Left]]) > 1:
                            # у предыдущего left еще есть правила
                            Left.Childrens = []
                            Left.Status = 'process'
                            LP[CV[Left]].pop()

                            retlenflag = False

                    else:
                        return None

                ind = 1
                continue





        #Если текущий разбор не совпал с токенами
        RS = RS[0: ind]
        confirmed = tokens[0: ind]
        if RS != confirmed or processFlag:

            processFlag = False # если попали сюда из-за не до конца разобранного дерева
                                # то препдолагаем что мы его доразберем на этой итерации

            #если можно разобрать текущю вершину
            if Left.Status == 'process':

                #проиндексировать вершину 

                if not Left in CV:
                    bufIndex = len(LP)
                    LP.append(GMAP[Left.Letter].copy())
                    CV[Left] = bufIndex

                #раскрыть Left по верхнему правилу из ее доступных (там точно есть правила, ведь мы ее только добавили)

                #создать список новых нод
                bufNewNodes = []

                for lettr in LP[CV[Left]][-1]:
                    newNode = None
                    #или терминал или нетерминал
                    if lettr in g.NonTerminals:
                        newNode = ATLNode('N', lettr)
                        prc += 1 #увеличить счетчик неразобранных нод
                    else:
                        newNode = ATLNode('T', lettr)

                    bufNewNodes.append(newNode)
                
                #присоединить созданные ноды к их папочке
                Left.AddChildrens(bufNewNodes)

                #установить родителю нод статус - разобран и уменьшить счетчик неразобранных нод
                Left.Status = 'ready'
                prc -=  1
                
                #смотрим дальше
                ind = 1
                continue

            #если текущая вершина уже разобрана
            else:

                #Левый ребенок не разобран?
                if Left.Childrens[0].Status == 'process' and Left.Childrens[0].TypeElement == 'N':

                    #Заносим текущую вершину в стек разбора
                    #и делаем левого ребенка текущим Left
                    LeftStack.append(Left)
                    Left = Left.Childrens[0]

                    #смотрим дальше 
                    ind = 1
                    continue

                #нет левого ребенка для разбора 
                else:

                    #попытаемся разобрать как-то по-другому, или переходить к родителям
                    #пока не сможем разобрать как-то по-другому их
                    #если разбирать как-то по-другому некого, то это - ошибка

                    flag = True

                    while flag:

                        #у Left есть еще правила которые можно использовать?
                        if len(LP[CV[Left]]) > 1:

                            #убить детей Left

                            Left.Childrens = []

                            LP[CV[Left]].pop()

                            #Сделать Left неразобранным
                            Left.Status = 'process'
                            prc += 1

                            
                            flag = False

                        #перебраны все правила для разбора
                        else:
                            # убить детей

                            Left.Childrens = []

                            #Обновить список доступных правил для разбора
                            LP[CV[Left]] = GMAP[Left.Letter].copy()

                            #теперь Left не разобран
                            Left.Status = 'process'
                            prc += 1

                            #если можно перейти к предыдущей вершине которую разбирали
                            if len(LeftStack) > 0:
                                #перейти можно
                                #переходим
                                
                                Left = LeftStack.pop()
                                1+1
                            else:
                                #перейти нельзя
                                #ошибка
                                return None


                    
                    
                    #идем дальше 
                    ind = 1
                    continue


        #Разбор совпадает с списком токенов до ind
        else:  

            #Left меняется на следующий неразобраный левый нетерменал



            if not Left in LeftStack:
                LeftStack.append(Left)

            Left = nextLeft(ROOT, Left) 

            ind += 1

            #если проверена всетокены
            if ind >= len(tokens) + 1:
                #если больше нет неразобранных нетерменалов
                #то все

                # TODO можно сделать счетчиком а не функцией для ускорения алгоритма

                prc = findPRC(ROOT)
                if prc == 0:
                    return retTree
                #если есть неразобранные нетерминалы 
                #переразбирать пока не останется неразобранных
                else:
                    processFlag = True
                    ind = 1
            
            #продолжить разбор
            continue
            



# testRoot = ATLNode('N', 'A')
# a = ATLNode('T', 'a')
# Blet = ATLNode('N', 'B')
# b = ATLNode('T', 'aa')
# c = ATLNode('T', 'cc')

# testRoot.AddChildrens([a, Blet])
# Blet.AddChildrens([b,c])

# rrrs = Rs(testRoot)

# print('test')



#new run


# g = Grammair()

# t = 'a,b'.split(',')
# n = 'S,A,B'.split(',')
# s = 'S'
# r = [
#     [['S'], ['A', 'B']],
#     [['A'], ['a', 'b']],
#     [['A'], ['a']],
#     [['B'], ['b']],
# ]

# fillGrammair(g, t, n, s, r)
# print(g)
# print(g.convertToDict())

# MyTree = createATLbyLL(g, ['a', 'b', 'b'], True)

# print('\nДерево')

# if MyTree:
#     MyTree.printTree()
# else:
#     print('невозможно построить')

# print('all')
