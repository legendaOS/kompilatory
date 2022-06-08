import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

graph = nx.Graph()

graph.add_node('A')
graph.add_node('B')
graph.add_node('C')

graph.add_edge('A', 'B')
graph.add_edge('A', 'C')

graph.add_node('D')
graph.add_node('E')
graph.add_node('F')

graph.add_edge('B', 'D')
graph.add_edge('B', 'E')
graph.add_edge('B', 'F')


graph.add_node('G')

graph.add_edge('C', 'G')

pos = graphviz_layout(graph, prog="twopi")
nx.draw(graph, pos)
plt.show()