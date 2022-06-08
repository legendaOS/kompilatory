import pptree 

root = pptree.Node('A')

pptree.Node('B', root)
pptree.Node('C', root)

pptree.print_tree(root, horizontal = False)

