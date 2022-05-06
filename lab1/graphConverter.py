def getNoda(note):
    return list(note.values())[0]

def getSymbol(note):
    return list(note.keys())[0]

class Graph():
    def __init__(self, startPoint, endPoint) -> None:
        self.Start = startPoint
        self.End = endPoint

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
        Map = {self.Start: {'Connections': self.Start.Connections, 'BackConnections': self.Start.BackConnections}}

        # index = 0
        # while True:
        #     #loop for append in Map

        #     Map[list(Map.keys())[index]]                        #текущий элемент в Map

        #     Map[list(Map.keys())[index]]['Connections']         # Connections in current element of Map
        #     Map[list(Map.keys())[index]]['BackConnections']     # Same

        #     ioc = 0                                             #index of connection in current element of connections in Map 

        #     while ioc < len(Map[list(Map.keys())[index]]['Connections'][ioc]):

        #         Map[list(Map.keys())[index]]['Connections'][ioc]
                

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


from itertools import count
from prettytable import PrettyTable  # Импортируем установленный модуль.

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

    



    return candidatesToRemove   
      








a = list('*|ab')

print(1)

b = createGraphFromList(a)




print(2)

c = b.createTable()

to_remove = deleteLongEps(b)

map = b.createMap()

poppo = map[list(map.keys())[0]]['Connections'][1][list(map[list(map.keys())[0]]['Connections'][0])[0]]
map[list(map.keys())[0]]['Connections']

l = b.getListOfNodes()



print('all')


