

def foo():
    i = 0
    while 1:
        yield i
        i += 1

a = foo()

for i in range(100): print(next(a))