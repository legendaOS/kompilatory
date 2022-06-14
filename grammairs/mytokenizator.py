def GetTokensByFile(fileName, myrezerved):
    f = open(fileName, 'r')
    stroka = f.read()

    buf = ''
    mytokens = []

    for letter in stroka:
        if letter in [' ', '\t']:
            if buf != '':
                mytokens.append(buf)
            buf = ''
        elif letter in ['\n', '\r']:
            if buf != '':
                mytokens.append(buf)
            mytokens.append(letter)
            buf = ''
        elif letter == ';':
            if buf != '':
                mytokens.append(buf)
            mytokens.append(letter)
            buf = ''
        else:
            buf += letter


    mynewtokens = []
    for tokind in range(len(mytokens)):
        if mytokens[tokind] in myrezerved:
            mynewtokens.append(mytokens[tokind])
        else:
            if tokind + 1 < len(mytokens) - 1:
                for lettr in mytokens[tokind]:
                    mynewtokens.append(lettr)
                if not mytokens[tokind + 1] in myrezerved:
                    mynewtokens.append(' ')

            else:
                for lettr in mytokens[tokind]:
                    mynewtokens.append(lettr)

    

    return mynewtokens