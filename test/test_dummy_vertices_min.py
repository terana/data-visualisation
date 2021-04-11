import pygraphml
import networkx as nx
import matplotlib.pyplot as plt

from datavis.CrossingsMinimisation import CrossingsMinimisation
from datavis.DummyVerticesMinimisation import DummyVerticesMinimisation


def test_dummy_vertices_min_and_crossings_min():
    parser = pygraphml.GraphMLParser()
    g = parser.parse("samples/dags/dag_13n.xml")

    dvm = DummyVerticesMinimisation(g)
    dvm.calculate_layers()
    dvm.dump_layers()

    cm = CrossingsMinimisation(dvm.layers)
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
