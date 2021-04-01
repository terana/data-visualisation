import pygraphml
import networkx as nx
import matplotlib.pyplot as plt
from datavis.Node import Node


class Graph:
    def __init__(self, root=None):
        self.root = root

    def load_graphml(self, graphml_file):
        # Not the fastest, but the easiest way...
        parser = pygraphml.GraphMLParser()
        g = parser.parse(graphml_file)

        # Searching for the root
        for node in g.nodes():
            if len(node.parent()) == 0:
                self.root = Node(id=node.id)
                g.set_root(node)
                break

        self._build_graph(g.root(), self.root)

    def _build_graph(self, pygraphml_node, node):
        children = pygraphml_node.children()

        if len(children) > 2:
            raise ValueError("Expect a binary tree.")

        if len(children) > 0:
            node.left = Node(id=children[0].id)
            self._build_graph(children[0], node.left)

        if len(children) > 1:
            node.right = Node(id=children[1].id)
            self._build_graph(children[1], node.right)

    def show(self, with_labels=False):
        def _add_node(g, n):
            g.add_node(n.id, pos=(n.x, -n.y))

            if n.left is not None:
                _add_node(g, n.left)
                g.add_edge(n.id, n.left.id)

            if n.right is not None:
                _add_node(g, n.right)
                g.add_edge(n.id, n.right.id)

        G = nx.DiGraph()
        _add_node(G, self.root)

        nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=with_labels, node_size=15)
        plt.show()
