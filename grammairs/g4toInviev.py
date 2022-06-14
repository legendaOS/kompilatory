from grammairs import Grammair

def createGrammairFromG4(fileName = 'C:/Users/grvla/Desktop/jyputer/kompilatory/grammairs/corundum.g4'):

    f = open(fileName, 'r')

    arr = f.read().split()

    f.close()

    index = 0
    while True:
        if arr[index] != ';' and arr[index][-1] == ';':
            buf = arr[index][0:-1]
            arr.pop(index)
            arr.insert(index, buf)
            index += 1
            arr.insert(index, ';')
        index += 1
        if index == len(arr):
            break


    

    newGramm = Grammair()

    leftPart = None
    rightBuf = []


    flagComma = False
    flagInComma = False
    bufNext = []
    bufComma = []



    for letter in arr:
        if flagComma:
            if flagInComma:
                if letter == ')':
                    flagInComma = False
                    continue
                if letter == '|': continue
                else:
                    bufComma.append(letter)
                
            else:
                if letter == ';':
                    #правило закончилось
                    flagComma = False
                    flagInComma = False

                    #добавить правила в грамматику
                    for microBufInComma in bufComma:
                        microBufRight = []
                        for mr in rightBuf:
                            microBufRight.append(mr)
                        microBufRight.append(microBufInComma)
                        for mr in bufNext:
                            microBufRight.append(mr)
                        
                        newGramm.setRule([leftPart], microBufRight)
                    
                    #обновить left
                    leftPart = None
                    1+1

                elif letter == '|':
                    #правило не закончилось
                    flagComma = False
                    flagInComma = False

                    #добавить правила в грамматику
                    for microBufInComma in bufComma:
                        microBufRight = []
                        for mr in rightBuf:
                            microBufRight.append(mr)
                        microBufRight.append(microBufInComma)
                        for mr in bufNext:
                            microBufRight.append(mr)
                        
                        newGramm.setRule([leftPart], microBufRight)

                else:
                    bufNext.append(letter)

        else:

            if leftPart:
                if letter == ':': continue
                if letter == '(': 
                    flagComma = True
                    flagInComma = True
                    bufNext = []
                    bufComma = []

                    continue

                elif letter == ';':
                    #вставить правила в грамматику
                    newGramm.setRule([leftPart], rightBuf)
                    rightBuf = []

                    leftPart = None
                    rightBuf = []
                    
                    
                elif letter == '|':
                    #вставить правила в грамматику
                    newGramm.setRule([leftPart], rightBuf)
                    rightBuf = []

                else:
                    #вставить в right buf
                    rightBuf.append(letter)

            else:
                leftPart = letter

                rightBuf = []


    
    
    nsymb = []
    tsymb = []

    for letter in arr:
        if not letter in [';', '|', '(', ')', ':']:
            if letter[0] != "\'":
                if not letter in nsymb:
                    nsymb.append(letter)
            else:
                if not letter[1:-1] in tsymb:
                    tsymb.append(letter[1:-1])

    for letter in nsymb:
        newGramm.setNonTerminal(letter)
    for letter in tsymb:
        newGramm.setTerminal(letter)

    newGramm.setStart('prog')



    """

        этих правил будет нехватать

        QUOTE : '\'';
        DQUOTE : '\"';

        CRLF : '\r' NEXT_LINE;
        CRLF : NEXT_LINE;

        NEXT_LINE : '\n'
        NEXT_LINE : '\n' NEXT_LINE;

        INT : [0-9]+;
        ->
        INT : [0-9] INT
        INT : [0-9]


        FLOAT : [0-9]*'.'[0-9]+; -> FLOAT: INT '.' INT

        ID : [a-zA-Z_][a-zA-Z0-9_]*; 
        -> ID : ALLSYMB list_of_symb
        -> ID : ALLSYMB

        ALLSYMB : [a-zA-Z_]+

        SYMB : [a-zA-Z0-9_]+;

        list_of_symb : ( SYMB | SYMB list_of_symb ); это правило есть

    """

    newGramm.setRule(['QUOTE'], ["\'"])
    newGramm.setRule(['DQUOTE'], ['\"'])

    newGramm.setRule(['CRLF'], ['\r', 'NEXT_LINE'])
    newGramm.setRule(['CRLF'], ['NEXT_LINE'])

    newGramm.setRule(['NEXT_LINE'], ['\n', 'NEXT_LINE'])
    newGramm.setRule(['NEXT_LINE'], ['\n'])

    for inta in range(10):
        newGramm.setRule(['INT'], [str(inta), 'INT'])
        newGramm.setRule(['INT'], [str(inta)])

    newGramm.setRule(['FLOAT'], ['INT', '.', 'INT'])


    azAZ_ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    azAZ_09 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'

    for stringa in azAZ_09:
        newGramm.setRule(['ALLSYMB'], [stringa])

    for stringa in azAZ_:
        newGramm.setRule(['SYMB'], [stringa])

    newGramm.setRule(['ID'], ['ALLSYMB', 'list_of_symb'])
    newGramm.setRule(['ID'], ['ALLSYMB'])

    #добавим новые нетерминалы в грамматику

    newGramm.setNonTerminal('NEXT_LINE')
    newGramm.setNonTerminal('ALLSYMB')

    #добавим служебные терминалы в грамматику

    newGramm.setTerminal('\r')
    newGramm.setTerminal('\n')
    newGramm.setTerminal('\'')
    newGramm.setTerminal('\"')
    newGramm.setTerminal('.')

    #соберем все терминалы в список зарезервированый символов

    Rezerved = []
    for lettr in newGramm.Terminals:
        Rezerved.append(lettr)


    #добавим новые терминалы (символы) в грамматику

    for stringa in azAZ_09:
        newGramm.setTerminal(stringa)


    ftog = open('C:/Users/grvla/Desktop/jyputer/kompilatory/grammairs/GRAMMAIR.txt', 'w')
    ftog.write(str(newGramm))

    ftog.close()

    return {'grammair' : newGramm, 'rezerved': Rezerved}