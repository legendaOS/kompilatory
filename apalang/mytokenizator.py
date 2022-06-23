def GetTokensByFile(fileName, myrezerved):
    f = open(fileName, 'r')
    stroka = f.read()

    
    mytokens = ''.join(stroka.split())

    mytokens.encode('cp1251')

    
    buffer = []
    endind = 1
    sind = 0
    while True:
        if mytokens[sind:endind] in myrezerved:
            buffer.append(mytokens[sind:endind])
            sind = endind
        endind += 1
        if endind == len(mytokens) + 1:
            break
        
    if sind + 1 != endind: return None

    return buffer