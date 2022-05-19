from graphConverter import *

print('Введите регулярное выражение')

s = input()

rs = convertToPoland(s)

g = NKAEps(rs)

print('НКА с эпсилонами')

prettyPrint(g.createTable())

NKA(g)

LOF = g.getListOfNodes()

print('НКА без эпсилонов')

prettyPrint(g.createTable())

k = DKA(g)

print('ДКА')

prettyPrint(k.createTable())

rerere = k.getListOfNodes()

mg = minGraph(k)

print('Минимальный ДКА')

prettyPrint(mg.createTable())

print('сделаны автоматы')

while True:
    print('введите строку для проверки')
    psn = input()
    
    flag = sumulation(k, psn)
    if flag:
        print('Прошла')
    else:
        print('Не прошла')

    