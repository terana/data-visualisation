from Graph import Graph
from LayeredTreeDraw import LayeredTreeDraw

g = Graph()
g.load_graphml("test_trees/tree-84n.xml")

ltd = LayeredTreeDraw(g)
ltd.set_coordinates()
ltd.show()
