import pygraphml
import networkx as nx
import matplotlib.pyplot as plt

from datavis.CoffmanGraham import CoffmanGraham
from datavis.CrossingsMinimisation import CrossingsMinimisation

if __name__ == "__main__":
    parser = pygraphml.GraphMLParser()
    g = parser.parse("samples/dags/dag_27n.xml")

    cg = CoffmanGraham(g, width=3)
    cg.calculate_layers(with_dummy_vertices=True)
    cg.damp_layers()

    cm = CrossingsMinimisation(cg.layers)
    cm.calculate()

    G = nx.DiGraph()
    for n in g.nodes():
        G.add_node(n.id, pos=(n.x, n.y), dummy=n.dummy)

    for e in g.edges():
        # The library doesn't allow to remove edges when we add dummy vertices.
        # This is a temporary workaround until I implement my own DAG implementation.
        if e.node1.y - e.node2.y < 2:
            G.add_edge(e.node1.id, e.node2.id)

    nx.draw(G, pos=nx.get_node_attributes(G, 'pos'),
            with_labels=False, node_size=[30 * int(not n.dummy) for n in g.nodes()])
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'), {n.id: n.id for n in g.nodes() if not n.dummy},
                            font_size=12, font_color='r')
    plt.show()
