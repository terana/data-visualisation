import pygraphml

from datavis.CoffmanGraham import CoffmanGraham


def test_coffman_graham_sanity():
    parser = pygraphml.GraphMLParser()
    g = parser.parse("samples/dags/dag_13n.xml")

    cg = CoffmanGraham(g, width=3)
    cg.calculate()
    cg.damp_layers()
