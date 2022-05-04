def parseString(s):
    
    #to do (a|b|(a|b|c))

    count = 0
    for i in s:
        if i == '(':
            count += 1
        if i == ")":
            count -= 1
        
    if count != 0: raise Exception('неверный формат строки')

    res = ''

    for index in range(len(s)):
        if s[index] != '|':
            if s[index] == '(':
                res += '['
            elif s[index] == ')':
                res += ']'
            else:
                res += s[index]
    return res




def parseList(s):
    ip = 0
    i = 0
    buf = None
    res = []

    for symb in s:
        ip = i
        if symb == '[':
            i += 1
        if symb == ']':
            i -= 1
        if i > ip:
            if buf != None:
                res.append(buf)
            buf = []
        if i < ip:
            if buf != None:
                res.append(buf)
            buf = None
        if i == ip:
            buf.append(symb)

    return res


k = parseList('[ab[abc]]')

print(k)