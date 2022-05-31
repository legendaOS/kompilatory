from grammairs import Grammair, fillGrammair
from bs4 import BeautifulSoup as Soup


class Parcer:
    def __init__(self) -> None:
        pass

    def INView(self, xmlFileName) -> Grammair:
        NONTERMINALS = []
        TERMINALS = []
        START = None
        RULES = []

        header = {'terminals': {}, 'nonterminals': [], 'start': None, 'rules': []}

        file = open(xmlFileName, 'r')
        doc = file.read()
        file.close()

        soup = Soup(doc)

        
        for ts in soup.find_all('term'):
            spell = ts.get('spell')
            name = ts.get('name')

            TERMINALS.append(spell)
            header['terminals'][name] = spell

        for nts in soup.find_all('nonterm'):
            name = nts.get('name')

            NONTERMINALS.append(name)
            header['nonterminals'].append(name)

        ss = soup.find('startsymbol')
        name = ss.get('name')
        START = name
        header['start'] = name


        RulesToHeader = []

        for rule in soup.find_all('production'):
            rhs = rule.find_all('symbol')
            lhs = rule.find('lhs').get('name')
            
            bufToHeaderRule = {'lhs': {'name': lhs}}
            bufToHeaderRule['rhs'] = []


            newRule = [[lhs]]
            rbuf = []
            for symb in rhs:
                

                sname = symb.get('name')
                stype = symb.get('type')

                bufToHeaderRule['rhs'].append({'name': sname, 'type': stype})

                if stype == 'nonterm':
                    rbuf.append(sname)

                else:
                    rbuf.append(header['terminals'][sname])

            newRule.append(rbuf)

            RULES.append(newRule)
            RulesToHeader.append(bufToHeaderRule)

        header['rules'] = RulesToHeader
        

        g = Grammair()
        fillGrammair(g, TERMINALS, NONTERMINALS, START, RULES)

        return({'Grammair': g, 'Header': header})


# p = Parcer()
# Bufer = p.INView('G0.xml')
# print(Bufer['Grammair'])

