from grammairs import *

# запишем грамматику G2 и присваивание в стиле Паскаля во внутреннее представление

g = Grammair()

p = [
    [['выражение'], ['арифметическоеВыражение', 'операцияОтношения','арифметическоеВыражение']],
    [['выражение'], ['арифметическоеВыражение']],
    [['арифметическоеВыражение'], ['арифметическоеВыражение', 'операцияТипаCложения', 'терм']],
    [['арифметическоеВыражение'], ['терм']],
    [['терм'], ['терм', 'операцияТипаУмножения', 'фактор']],
    [['терм'], ['фактор']],
    [['фактор'], ['var']],
    [['фактор'], ['const']],
    [['фактор'], ['(', 'арифметическоеВыражение', ')']],
    [['операцияОтношения'], ['<']],
    [['операцияОтношения'], ['<=']],
    [['операцияОтношения'], ['=']],
    [['операцияОтношения'], ['<>']],
    [['операцияОтношения'], ['>']],
    [['операцияОтношения'], ['>=']],
    [['операцияТипаCложения'], ['+']],
    [['операцияТипаCложения'], ['-']],
    [['операцияТипаУмножения'], ['*']],
    [['операцияТипаУмножения'], ['/']],
]

n = [
    'выражение',
    'арифметическоеВыражение',
    'операцияОтношения',
    'операцияТипаCложения',
    'терм',
    'операцияТипаУмножения',
    'фактор',
]

t = [
    'var',
    'const',
    '(', ')',
    '<', '<=', '=', '<>', '>', '>=', '+', '-', '*', '/'
]

s = 'выражение'

fillGrammair(g, t, n, s, p)

print(g)

# удалить левую рекурсию

deleteAllLeftRecursion(g)

print('-------------------------------------------------------')
print('-------------------------------------------------------')

print(g)

# попробуем разобрать примеры
# var + var
# const = var * ( var + var )

from ATLcreate import *


tokens1 = 'var * var * var'.split(' ')

MyTree1 = LLRecursion(g, tokens1, True)

# TODO выбирать не самую левую а любую неразобранную кроме правой

print('Дерево по токенам', tokens1)
if MyTree1:
    MyTree1.printTree()
else:
    print('невозможно построить')




