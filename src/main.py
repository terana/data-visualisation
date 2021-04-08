from datavis.Graph import Graph
from datavis.LayeredTreeDraw import LayeredTreeDraw

g = Graph()
g.load_graphml("test_files/bitrees/tree-828n.xml")

ltd = LayeredTreeDraw(g)
ltd.set_coordinates()
ltd.show()
