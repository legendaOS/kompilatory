from ast import Try


class Graph():
    def __init__(self, startPoint, endPoint) -> None:
        self.Start = startPoint
        self.End = endPoint

class Node():
    def __init__(self) -> None:
        self.Connections = []
    
    def appendConnection(self, letter, pointToConnect):
        self.Connections.append({letter: pointToConnect})


def createLetterGraph(letter: str) -> Graph:
    """
        Создание графа по типу "символ", на вход принимает символ
    """
    localStartPoint = Node()
    localEndPoint = Node()

    localStartPoint.appendConnection(letter, localEndPoint)

    return Graph(localStartPoint, localEndPoint)


def createConcatGraph(g1: Graph, g2 : Graph) -> Graph:
    g1.End.appendConnection('eps', g2.Start)

    return Graph(g1.Start, g2.End)

def createOrGraph(listOfGraphs) -> Graph:
    localStartPoint = Node()
    localEndPoint = Node()

    for iterGraph in listOfGraphs:
        localStartPoint.appendConnection('eps', iterGraph.Start)
        iterGraph.End.appendConnection('eps', localEndPoint)

    return Graph(localStartPoint, localEndPoint)


def createStarGraph(g:Graph) -> Graph:
    localStartPoint = Node()
    localEndPoint = Node()

    localStartPoint.appendConnection('eps', localEndPoint)
    localStartPoint.appendConnection('eps', g.Start)
    g.End.appendConnection('eps', localEndPoint)
    g.End.appendConnection('eps', g.Start)

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
        
        elif listTograph[index] == '|':
            pass
        elif listTograph[index] == '*':
            pass

    return listTograph[0]



a = list('.ab')

b = createGraphFromList(a)


print('all')
    


