from g4toInviev import *
from grammairs import *
from mytokenizator import *



bufGrammair = createGrammairFromG4()

mytokens = GetTokensByFile('C:/Users/grvla/Desktop/jyputer/kompilatory/grammairs/test.rb', bufGrammair['rezerved'])

print('all')

newGramm = bufGrammair['grammair']

from ATLcreate import *

MyTree1 = LLRecursion(newGramm, mytokens, debug=True)
1+1
print('all')