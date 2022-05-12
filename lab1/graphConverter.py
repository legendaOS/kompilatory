def getNoda(note):
    return list(note.values())[0]

def getSymbol(note):
    return list(note.keys())[0]

def getAllNodes(connection):
    buf = []
    for i in connection:
        buf.append(getNoda(i))
    return buf

class Graph():
    def __init__(self, startPoint, endPoint) -> None:
        self.Start = startPoint
        self.End = endPoint
        self.Finish = []

    def getListOfNodes(self):
        numeratedNodes = [self.Start]
        connectionsSymbols = []
        index = 0
        while True:

            connectedNodes = []
            countOfAppended = 0

            for nodeInCurrentConnections in numeratedNodes[index].Connections:
                connectedNodes.append(list(nodeInCurrentConnections.values())[0])
                connectionsSymbols.append(list(nodeInCurrentConnections.keys())[0])

            for nodeInCurrentConnections in connectedNodes:
                if not nodeInCurrentConnections in numeratedNodes:
                    numeratedNodes.append(nodeInCurrentConnections)
                    countOfAppended += 1

            if countOfAppended == 0 and index == len(numeratedNodes) - 1:
                break
            else:
                index += 1

        return {'numeratedNodes': numeratedNodes, 'connectionsSymbols': list(set(connectionsSymbols))}


    def createMap(self):
        listAllNodes = [self.Start]
        Map = {}

        index = 0

        while True:
            appended = 0

            Map[listAllNodes[index]] = {'Connections': listAllNodes[index].getConnections(), 'BackConnections': listAllNodes[index].getBackConnections()}
            
            for i in getAllNodes(Map[listAllNodes[index]]['Connections']):
                if not i in listAllNodes:
                    listAllNodes.append(i)

            

            index += 1

            if index == len(listAllNodes): break

        return Map


    def createTable(self):
        listOfNodes = self.getListOfNodes()
        sumbHref = listOfNodes['connectionsSymbols']

        returnsTable = []

        annotation = {}
        for i in range(len(sumbHref)):
            annotation[sumbHref[i]] = i


        for element in listOfNodes['numeratedNodes']:
            columnToInsert = [[] for i in range(len(sumbHref))]
            for oneConnect in element.Connections:
                columnToInsert[annotation[list(oneConnect.keys())[0]]].append(listOfNodes['numeratedNodes'].index(list(oneConnect.values())[0]))
            returnsTable.append(columnToInsert)


        return {'table': returnsTable, 'annotation': sumbHref}


class Node():
    def __init__(self) -> None:
        self.Connections = []
        self.BackConnections = []

    
    def appendConnection(self, letter, pointToConnect):
        self.Connections.append({letter: pointToConnect})

    def appendBackConnections(self, letter, pointToConnect):
        self.BackConnections.append({letter: pointToConnect})

    def getConnections(self):
        return self.Connections

    def getBackConnections(self):
        return self.BackConnections



def createLetterGraph(letter: str) -> Graph:
    """
        Создание графа по типу "символ", на вход принимает символ
    """
    localStartPoint = Node()
    localEndPoint = Node()

    localStartPoint.appendConnection(letter, localEndPoint)
    localEndPoint.appendBackConnections(letter, localStartPoint)



    return Graph(localStartPoint, localEndPoint)


def createConcatGraph(g1: Graph, g2 : Graph) -> Graph:
    g1.End.appendConnection('eps', g2.Start)

    g2.Start.appendBackConnections('eps', g1.End)


    return Graph(g1.Start, g2.End)

def createOrGraph(listOfGraphs) -> Graph:
    localStartPoint = Node()
    localEndPoint = Node()

    for iterGraph in listOfGraphs:
        localStartPoint.appendConnection('eps', iterGraph.Start)
        iterGraph.Start.appendBackConnections('eps', localStartPoint)



        iterGraph.End.appendConnection('eps', localEndPoint)

        localEndPoint.appendBackConnections('eps', iterGraph.End)

    return Graph(localStartPoint, localEndPoint)


def createStarGraph(g:Graph) -> Graph:
    localStartPoint = Node()
    localEndPoint = Node()

    localStartPoint.appendConnection('eps', localEndPoint)

    localEndPoint.appendBackConnections('eps', localStartPoint)

    localStartPoint.appendConnection('eps', g.Start)

    g.Start.appendBackConnections('eps', localStartPoint)

    g.End.appendConnection('eps', localEndPoint)

    localEndPoint.appendBackConnections('eps', g.End)

    g.End.appendConnection('eps', g.Start)

    g.Start.appendBackConnections('eps', g.End)

    return Graph(localStartPoint, localEndPoint)


def allSymbToGraphs(convertedList, sepcSymbolls = ['|', '.', '*']):
    ret = []
    for element in convertedList:
        if not element in sepcSymbolls:
            ret.append(createLetterGraph(element))
        else:
            ret.append(element)

    return ret


def createGraphFromList(convertedList):
    listTograph = allSymbToGraphs(convertedList)
    index = 0

    while len(listTograph) != 1:

        if listTograph[index] == '.':
            if type(listTograph[index+1]) == Graph and type(listTograph[index+2]) == Graph:
                listTograph[index] = createConcatGraph(listTograph[index+1], listTograph[index+2])
                listTograph.pop(index+1)
                listTograph.pop(index+1)
            else:
                index += 1
        
        elif listTograph[index] == '|':
            if type(listTograph[index+1]) == Graph and type(listTograph[index+2]) == Graph:
                listTograph[index] = createOrGraph([listTograph[index+1], listTograph[index+2]])
                listTograph.pop(index+1)
                listTograph.pop(index+1)
            else:
                index += 1

        elif listTograph[index] == '*':
            if type(listTograph[index+1]) == Graph:
                listTograph[index] = createStarGraph(listTograph[index+1])
                listTograph.pop(index+1)
            else:
                index += 1

        else:
            if index == len(listTograph) - 1:
                index = 0
            else:
                index += 1

    return listTograph[0]

from prettytable import PrettyTable


def prettyPrint(tableWithAnnotation):
    th = ['N']
    for i in tableWithAnnotation['annotation']: th.append(i)

    td = []
    index = 0
    for column in tableWithAnnotation['table']:
        td.append(str(index))
        for elem in column:
            if elem == []:
                td.append('-')
            else:
                td.append(','.join([str(i) for i in elem]))
        index += 1

    columns = len(th)
    table = PrettyTable(th)
    td_data = td[:]
    while td_data:
        table.add_row(td_data[:columns])
        td_data = td_data[columns:]

    print(table)  # Печатаем таблицу


def deleteLongEps(g: Graph):
    listOfnodes = g.getListOfNodes()['numeratedNodes']
    reconnections = {}
    candidatesToRemove = []

    for node in listOfnodes:
        listOfEpsConnections = []

        for elem in node.Connections:
            if list(elem.keys())[0] == 'eps':
                listOfEpsConnections.append(list(elem.values())[0])

        reconnections[node] = listOfEpsConnections

        index = 0

        if len(reconnections[node]) == 0:
            continue

        while True:
            listOfEpsConnections = []
            countOfAppend = 0
            for elem in reconnections[node][index].Connections:
                if list(elem.keys())[0] == 'eps':
                    noda = list(elem.values())[0]
                    listOfEpsConnections.append(noda)
                    countOfAppend += 1
                    if not reconnections[node][index] in candidatesToRemove:
                        candidatesToRemove.append(reconnections[node][index])
                    
            for elemToAppend in listOfEpsConnections:
                reconnections[node].append(elemToAppend)

            if countOfAppend == 0 and index == len(reconnections[node]) - 1:
                break
            else:
                index += 1

    
    graphMap = g.createMap()

    #добавить новые епс соединения из списка новых соединений

    for key in reconnections.keys():
        for new_connect in reconnections[key]:
            if not new_connect in getAllNodes(graphMap[key]['Connections']):
                graphMap[key]['Connections'].append({'eps': new_connect})


    #delete all connections and backconnections to candidates to remove
    
    for node in graphMap.keys():
        index_in_node = 0
        while True:
            if len(graphMap[node]['Connections']) > 0:
                if getNoda(graphMap[node]['Connections'][index_in_node]) in candidatesToRemove:
                    graphMap[node]['Connections'].pop(index_in_node)
                else:
                    index_in_node += 1
            if index_in_node >= len(graphMap[node]['Connections']): break

        index_in_node = 0
        while True:
            if len(graphMap[node]['BackConnections']) > 0:
                if getNoda(graphMap[node]['BackConnections'][index_in_node]) in candidatesToRemove:
                    graphMap[node]['BackConnections'].pop(index_in_node)
                else:
                    index_in_node += 1
            if index_in_node >= len(graphMap[node]['BackConnections']): break

    
    #Создать конечную точку и добавить новые конечные точки

    candidatesToFinish = [g.End]
    while True:
        appended = 0
        for node in graphMap.keys():
            for connect in graphMap[node]['Connections']:
                if getNoda(connect) in candidatesToFinish and getSymbol(connect) == 'eps' and not node in candidatesToFinish:
                    candidatesToFinish.append(node)
                    appended += 1
        if appended == 0:
            break

    for i in candidatesToFinish:
        g.Finish.append(i)

    #рекомпановка соединений через епсилоны

    
      


def recomposition(g: Graph):
    graphMap = g.createMap()

    recomposition = {}

    for noda in graphMap.keys():
        epsilons = [] #list on nodes
        for connection in noda.getConnections():
            if getSymbol(connection) == 'eps':
                epsilons.append(getNoda(connection))
        next = [] #list of list of connections
        for eps_noda in epsilons:
            buffer_connections = []
            for connection in eps_noda.getConnections():
                if getSymbol(connection) != 'eps':
                    buffer_connections.append(connection)
            next.append(buffer_connections)
        recomposition[noda] = {'epsilons': epsilons, 'next':next}

    

    for noda in recomposition:
        #уалить эпсилон переходы из начала
        for epsilon_noda_index in range(len(recomposition[noda]['epsilons'])):
            epsilon_noda = recomposition[noda]['epsilons'][epsilon_noda_index]
            if len(recomposition[noda]['next'][epsilon_noda_index]):
                c_i_b = graphMap[noda]['Connections'] 
                if {'eps': epsilon_noda} in c_i_b:
                    c_i_b.pop(c_i_b.index({'eps': epsilon_noda}))
        
        #удалить буквенные переходы после епсилон переходад
        for i_it_c in range(len(recomposition[noda]['next'])):
            list_con = recomposition[noda]['next'][i_it_c]
            if list_con != []:
                for iter_con in list_con:
                    del_name = recomposition[noda]['epsilons'][i_it_c]
                    gr_con = graphMap[del_name]['Connections']
                    buf = {getSymbol(iter_con): getNoda(iter_con)}
                    if buf in gr_con:
                        gr_con.pop(gr_con.index(buf))

        # соединение нод между которыми разорваны связи
        for i_it_c in range(len(recomposition[noda]['next'])):
            list_con = recomposition[noda]['next'][i_it_c]
            if list_con != []:
                for iter_con in list_con:
                    gr_con = graphMap[noda]['Connections']
                    buf = {getSymbol(iter_con): getNoda(iter_con)}
                    if not buf in gr_con:
                        gr_con.append(buf)

    # return graphMap
    return recomposition


def deleteEpsConnections(g: Graph):
    graphMap = g.createMap()

    for noda in graphMap:
        index = 0
        if len(graphMap[noda]['Connections']) != 0:
            while True:
                if getSymbol(graphMap[noda]['Connections'][index]) == 'eps':
                    graphMap[noda]['Connections'].pop(index)
                else:
                    index += 1
                if index == len(graphMap[noda]['Connections']): break
    
    nodes = g.getListOfNodes()['numeratedNodes']

    index = 0
    if g.Finish != []:
        while True:
            if not g.Finish[index] in nodes:
                g.Finish.pop(index)
            else:
                index += 1
            if index == len(g.Finish): break 


def NKAEps(parsedPoland: list):
    return createGraphFromList(parsedPoland)

def NKA(g:Graph):
    deleteLongEps(g)
    recomposition(g)
    deleteEpsConnections(g)

def getConnectionsInMap(Map, node):
    return Map[node]['Connections']

def convTIntL(a):
    k = a[1:-1].split(', ')
    return list(int(i) for i in k)

def DKA(g:Graph):
    nodes = g.getListOfNodes()['numeratedNodes']
    letters = g.getListOfNodes()['connectionsSymbols']

    numbers = {}
    newConnections = {}

        
    for i in range(len(nodes)): numbers[nodes[i]] = i

    Qstack = [[numbers[g.Start]]]

    index = 0
    while True:
        iterNodes = []
        for i in Qstack[index]: iterNodes.append(nodes[i])
        

        iterConnections = []
        for noda in iterNodes:
            for connection in noda.getConnections():
                iterConnections.append(connection)

        bufferConnections = {}
        for i in letters:
            bufferConnections[i] = []
        for i in iterConnections:
            if not numbers[getNoda(i)] in bufferConnections[getSymbol(i)]:
                bufferConnections[getSymbol(i)].append(numbers[getNoda(i)])

        for i in bufferConnections.keys():
            bufferConnections[i].sort()

        


        newConnections[str(Qstack[index])] = bufferConnections
        for i in bufferConnections.values():
            if not i in Qstack: Qstack.append(i)


        
        
        index += 1
        if index == len(Qstack): break
                  

    fin = []
    for i in g.Finish:
        fin.append(numbers[i])

    #create DKA

    for i in newConnections.keys():
        for k in newConnections[i].keys():
            newConnections[i][k] = str(newConnections[i][k])

    sp = None
    resGraph = None
    newPoints = {}



    deleted_keys = []

    for key in newConnections.keys():
        if key == '[]':
            deleted_keys.append(key)

    for key in deleted_keys:
        newConnections.pop(key)



    deleted_keys = {}

    for key in newConnections.keys():
        deleted_keys[key] = []
        for key_in in newConnections[key]:
            if newConnections[key][key_in] == '[]':
                deleted_keys[key].append(key_in)



    for key in deleted_keys.keys():
        for key_in in deleted_keys[key]:
            newConnections[key].pop(key_in)


    for nodeName in newConnections.keys():
        if 0 in convTIntL(nodeName):
            sp = Node()
            resGraph = Graph(sp, sp)
            newPoints[nodeName] = sp
        else:
            newPoints[nodeName] = Node()
        
    for nodeName in newPoints.keys():
        for i in fin:
            if i in convTIntL(nodeName):
                resGraph.Finish.append(newPoints[nodeName])


    for nodeName in newConnections.keys():
        for letterConnection in newConnections[nodeName].keys():
            newPoints[nodeName].appendConnection(letterConnection, newPoints[newConnections[nodeName][letterConnection]])
    
    return resGraph


def sumulation(g: Graph, reg: str) -> bool:
    currentNode = g.Start
    for letter in reg:
        connections_in = currentNode.getConnections()
        flagHas = False
        index = None
        for index_connect in range(len(connections_in)):
            if getSymbol(connections_in[index_connect]) == letter:
                flagHas = True
                index = index_connect
                break
        if flagHas:
            currentNode = getNoda(connections_in[index])
        else:
            return False

    if currentNode in g.Finish:
        return True
    else:
        return False


def convertToPoland(s:str) -> str:
    #расставить точки
    operators = ['*', '|']
    alloperators = ['*', '(', ')', '|']
    allop = ['*', ')', '|']
    buf = ''
    for i in range(len(s) - 1):
        if s[i] == ')':
            if not s[i+1] in allop:
                buf += s[i]
                buf += '.'
            else:
                buf += s[i]
        elif not s[i] in alloperators:
            if not s[i+1] in allop:
                buf += s[i]
                buf += '.'
            else:
                buf += s[i]
        elif s[i] == '*':
            buf += s[i]
            buf += '.'
        else:
            buf += s[i]
        
    buf += s[-1]

    nbuf = ''
    for i in buf[::-1]:
        if i == ')':
            nbuf+= '('
        elif i == '(':
            nbuf += ')'
        else:
            nbuf += i
    
    #convert to polka

    ops = ['(', ')', '.', '|', '*']
    
    prioritet = {'.': 1, '|':2, '*': 3, '(': 0}
    rets = ''
    Qstack = []

    for let in nbuf:

        if not let in ops:
            rets += let
        else:
            if let == '(':
                Qstack.append(let)
            elif let == ')':
                while True:
                    ntr = Qstack.pop()
                    if ntr == '(': 
                        break
                    else:
                        rets += ntr
            else:
                if len(Qstack) == 0:
                    Qstack.append(let)
                else:
                    if prioritet[let] > prioritet[Qstack[-1]]:
                        Qstack.append(let)
                    else:
                        while True:
                            top = Qstack[len(Qstack)-1]
                            priortop = prioritet.get(top)
                            priorlet = prioritet.get(let)
                            if priortop <= priorlet and len(Qstack) != 0:
                                ntr = Qstack.pop()
                                rets += ntr
                            else:
                                break
                        Qstack.append(let)


    while True:
        if len(Qstack) != 0:
            rets += Qstack.pop()
        else:
            break

    

    return rets[::-1]


def decart(s1,s2):
   return list([[a,b] for a in s1 for b in s2])

def andReplace(s):
    buf = s.copy()
    buf2 = list([[i[1], i[0]] for i in s])
    buf.extend(buf2)
    return buf


def minGraph(g: Graph) -> Graph:
    nodeList = g.getListOfNodes()

    gTable = g.createTable()
    
    index = 0
    nameOfNodes = {}
    for noda in nodeList['numeratedNodes']:
        nameOfNodes[noda] = index
        index += 1

    marked = []
    Qstack = []

    nameOfFinishes = []
    for noda in g.Finish:
        nameOfFinishes.append(nameOfNodes[noda])

    for noda in nodeList['numeratedNodes']:
        bufStr = []
        for noda_in in nodeList['numeratedNodes']:
            if nameOfNodes[noda] == nameOfNodes[noda_in]:
                bufStr.append(False)
            else:
                if nameOfNodes[noda] in nameOfFinishes:
                    if nameOfNodes[noda_in] in nameOfFinishes:
                        bufStr.append(False)
                    else:
                        bufStr.append(True)
                        Qstack.append([nameOfNodes[noda_in], nameOfNodes[noda]])
                else:
                    if nameOfNodes[noda_in] in nameOfFinishes:
                        bufStr.append(True)
                        Qstack.append([nameOfNodes[noda_in], nameOfNodes[noda]])
                    else:
                        bufStr.append(False)
        marked.append(bufStr)

    #создать дельту
    delta = []

    terminals = []
    for t in gTable['annotation']:
        terminals.append(t)
    
    for noda in nodeList['numeratedNodes']:

        bufStr = []
        for letter in terminals:
            bufLetter = []
            for connect in noda.getConnections():
                if getSymbol(connect) == letter:
                    bufLetter.append(nameOfNodes[getNoda(connect)])
            bufStr.append(bufLetter)
        delta.append(bufStr)

    #обновить marked по delta

    for noda in nodeList['numeratedNodes']:
        strName = nameOfNodes[noda]
        for noda_in in nodeList['numeratedNodes']:
            stlbName = nameOfNodes[noda_in]

            if marked[strName][stlbName] == False:
                buf = []

                for index in range(len(terminals)):
                    if delta[strName][index] != [] and delta[stlbName][index] != []:
                        buf.extend( andReplace(decart(delta[strName][index], delta[stlbName][index])) )
                

                for elem in buf:
                    if marked[elem[0]][elem[1]] or marked[elem[1]][elem[0]]:
                        marked[strName][stlbName] = True
                        marked[stlbName][strName] = True
                        break



    #создать deltaminus

    deltaminus = []

    for noda in nodeList['numeratedNodes']:

        bufStr = []
        for i in terminals:
            bufStr.append([])
        deltaminus.append(bufStr)

    for noda in nodeList['numeratedNodes']:
        for connect in noda.getConnections():
            deltaminus[nameOfNodes[getNoda(connect)]][terminals.index(getSymbol(connect))].append(nameOfNodes[noda])


    #удалить все из Qstack и обновить marked по deltaminus

    while True:
        if len(Qstack) != 0:
            para = Qstack.pop()
            if marked[para[0]][para[1]] == False or marked[para[1]][para[0]] == False:
                buf = []
                for ind_l in range(len(terminals)):
                    if deltaminus[para[0]][ind_l] != [] and deltaminus[para[1]][ind_l] != []:
                        buf.extend(andReplace(decart(deltaminus[para[0]][ind_l], deltaminus[para[1]][ind_l])))

                for elem in buf:
                    if marked[elem[0]][elem[1]] == False or marked[elem[1]][elem[0]] == False:
                        marked[elem[0]][elem[1]] = True
                        marked[elem[1]][elem[0]] = True
                        Qstack.append(elem)
        else:
            break


    #выбрать компоненты

    components = []

    for stroka in marked:
        bufTocomp = []
        for index in range(len(stroka)):
            if stroka[index] == False:
                bufTocomp.append(index)
        if not bufTocomp in components:
            components.append(bufTocomp)
    
    componentsFromNodes = []

    for comp in components:
        bufTocomp = []
        for c_in in comp:
            bufTocomp.append(nodeList['numeratedNodes'][c_in])
        componentsFromNodes.append(bufTocomp)

    #собрать граф
    
    points = []

    mapa = {}
    for index_comp in range(len(componentsFromNodes)):
        comp = componentsFromNodes[index_comp]
        for noda in comp:
            mapa[noda] = index_comp

    for comp in componentsFromNodes:
        points.append(Node())
        

    for index_comp in range(len(componentsFromNodes)):
        comp = componentsFromNodes[index_comp]
        for noda in comp:
            for connect in noda.getConnections():
                points[index_comp].appendConnection(getSymbol(connect), points[mapa[getNoda(connect)]])



    retG = Graph(points[0], points[0])

    bufFin = []
    for index in range(len(components)):
        comp = components[index]
        for elem in comp:
            if elem in nameOfFinishes:
                if not index in bufFin:
                    bufFin.append(index)

    f = []
    for elm in bufFin:
        f.append(points[elm])

    retG.Finish = f

    mapping = retG.createMap()

    for noda in retG.getListOfNodes()['numeratedNodes']:
        buf = noda.getConnections()
        buf1 = []
        for i in buf:
            if not i in buf1:
                buf1.append(i)
        while True:
            noda.getConnections().pop()
            if len(noda.getConnections()) == 0: break
        for i in buf1:
            noda.getConnections().append(i)
        
                
    return retG



kk = [1,2]
kj = [3,4,5]
ff = andReplace(decart(kk, kj))

s = convertToPoland('(a|b)*c|d')    

a = ".a*|bc"

g = NKAEps(a)

prettyPrint(g.createTable())

NKA(g)

LOF = g.getListOfNodes()

prettyPrint(g.createTable())

DKA = DKA(g)

prettyPrint(DKA.createTable())

rerere = DKA.getListOfNodes()

minG = minGraph(DKA)

prettyPrint(minG.createTable())

flag = sumulation(minG, 'bc')

print('all')