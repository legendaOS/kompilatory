from ATLcreate import ATLTree, Shstr

def convertToJS(Ctree: ATLTree) -> str:
    stack = []
    stackFunctions = []

    allNodes = Shstr(Ctree.Root)

    convertTerminals = {
        "пока": 'while', "выполнять" : '{', "все": '};', "стоп" : 'break', "функция" : 'function', 
        "вернуть": 'return', "если" : 'if', "иначе" : 'else', "для" : 'for', "до" : "", "внутри" : "", "шаг" : "",
        "начало" : "async function main(){", "конец":'}; main(); rl.close();', "получить": "await getl(", 'вставить': "await add(", "продолжить": 'continue'
    }

    probelnNT = ['Функция', 'Пока', 'Для', 'Если', 'Продолжить', 'Стоп', 'Вставить', 'Блок', 'СписокБлоков', 'Определение', 
    'Объявление', 'Присваивание', 'Программа', 'Получить', 'Ввод', 'Вывод']

    for noda in allNodes[0:-1]:

        Letter = noda.Letter
        NType = noda.TypeElement

        if NType == 'T':
            if Letter in convertTerminals:
                stack.append(convertTerminals[Letter])
            else:
                stack.append(Letter)
        else:
            LENG = len(noda.Childrens)
            buf = []
            for i in range(LENG):
                buf.append(stack.pop())

            rightBuf = buf[::-1]

            #разобрать красавцев ломающих структуру жс

            if Letter == 'Вставить':
                z = ','
                k = ')'
                nBuf = f'{rightBuf[0]} {rightBuf[1]} {z} {rightBuf[3]} {k}'
                stack.append(nBuf)
                1+1

            elif Letter == 'Получить':
                z = ','
                k = ')'
                nbuf = f'{rightBuf[0]} {rightBuf[1]} {z} {rightBuf[3]} {k}'
                stack.append(nbuf)

            elif Letter == 'Если':
                if LENG == 5:
                    nbuf = f'{rightBuf[0]} ({rightBuf[1]}) {rightBuf[2]} {rightBuf[3]} {rightBuf[4]}'
                    stack.append(nbuf)
                else:
                    z = '}'
                    l = '{'
                    nbuf = f'{rightBuf[0]} ({rightBuf[1]}) {rightBuf[2]} {rightBuf[3]} {z} {rightBuf[4]} {l} {rightBuf[5]} {rightBuf[6]}'
                    stack.append(nbuf)

            elif Letter == 'Пока':
                nbuf = f'{rightBuf[0]} {rightBuf[1]} {rightBuf[2]} ({rightBuf[3]}) {rightBuf[4]} {rightBuf[5]} {rightBuf[6]}'
                stack.append(nbuf)

            elif Letter == 'Функция':
                stackFunctions.append('async ' + ' '.join(rightBuf))
                stack.append('async ' + ' '.join(rightBuf))
                1+1

            elif Letter == 'Для':
                if LENG == 11:
                    nbuf = f'{rightBuf[0]} {rightBuf[1]} {rightBuf[2]} ( {rightBuf[3]} ; '
                    nbuf += f'{rightBuf[3]} < {rightBuf[5]} ; {rightBuf[3]} = {rightBuf[3]} + {rightBuf[7]} ) '
                    nbuf += f'{rightBuf[8]} {rightBuf[9]} {rightBuf[10]}'
                    stack.append(nbuf)
                else:
                    nbuf = f'{rightBuf[0]} {rightBuf[1]} {rightBuf[2]} ( '
                    nbuf += f'{rightBuf[3]} of {rightBuf[5]} ) {rightBuf[6]} {rightBuf[7]} {rightBuf[8]}'
                    stack.append(nbuf)

            elif Letter == 'Определение':
                nbuf = ''
                if rightBuf[0] == 'список':
                    nbuf = f'let {rightBuf[1]} = [] '
                else:
                    nbuf = f'let {rightBuf[1]}'
                stack.append(nbuf)

            elif Letter == 'Объявление':
                nbuf = f''
                if rightBuf[0] == 'целое':
                    nbuf = f'let {rightBuf[1]} = parseInt({rightBuf[3]})'
                elif rightBuf[0] == 'дробное':
                    nbuf = f'let {rightBuf[1]} = parseFloat({rightBuf[3]})'
                elif rightBuf[0] == 'строка':
                    nbuf = f'let {rightBuf[1]} = "" + {rightBuf[3]}'
                else:
                    nbuf = f'let {rightBuf[1]} = {rightBuf[3]}'
                stack.append(nbuf)

            elif Letter == 'Вызов':
                nbuf = f'await {rightBuf[0]} {rightBuf[1]} {rightBuf[2]}'
                stack.append(nbuf)

            elif Letter == 'Ввод':
                nbuf = f'{rightBuf[1]} = await ВВОД()'
                stack.append(nbuf)

            elif Letter == 'Вывод':
                nbuf = f'await ВЫВОД({rightBuf[1]})'
                stack.append(nbuf)

            else:
                if Letter in probelnNT:
                    stack.append(' '.join(rightBuf))
                else:
                    stack.append(''.join(rightBuf))

    stack = [' '.join(stack)]

    rs = stack[0]
    for pdstr in stackFunctions:
        rs = rs.replace(pdstr, '')

    return ([rs , stackFunctions])


def createJsStringNode(mainstr, functionsList):
    pass
