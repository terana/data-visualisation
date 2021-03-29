import pygraphml
import networkx as nx
import matplotlib.pyplot as plt


parser = pygraphml.GraphMLParser()
g = parser.parse("test_trees/tree-3n.xml")

G = nx.DiGraph()

G.add_node("n0", pos=(0, 0))
G.add_node("n1", pos=(-50, -50))
G.add_node("n2", pos=(50, -50))


G.add_edge("n0", "n1")
G.add_edge("n0", "n2")
nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=50)
plt.show()
