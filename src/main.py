from datavis.BiTree import BiTree
from datavis.LayeredTreeDraw import LayeredTreeDraw

g = BiTree()
g.load_graphml("test_files/bitrees/tree-828n.xml")

ltd = LayeredTreeDraw(g)
ltd.set_coordinates()
ltd.show()
